import requests
from django.utils import timezone

from core.models import PlatformAccount, UserStats

LEETCODE_GRAPHQL = "https://leetcode.com/graphql"


# =========================================
# GraphQL Fetch
# =========================================
def get_leetcode_stats(username: str):

    query = """
    query getUserProfile($username: String!) {
      matchedUser(username: $username) {
        submitStatsGlobal {
          acSubmissionNum {
            difficulty
            count
          }
        }
      }
      userContestRanking(username: $username) {
        rating
        attendedContestsCount
      }
    }
    """

    r = requests.post(
        LEETCODE_GRAPHQL,
        json={"query": query, "variables": {"username": username}},
        headers={
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com"
        },
        timeout=15
    )

    r.raise_for_status()
    data = r.json()

    user = data.get("data", {}).get("matchedUser")
    if not user:
        raise Exception("LeetCode user not found")

    # -------------------------
    # Difficulty buckets
    # -------------------------
    easy = 0
    medium = 0
    hard = 0
    solved_total = 0

    buckets = user.get("submitStatsGlobal", {}).get("acSubmissionNum", [])

    for row in buckets:
        diff = row.get("difficulty", "").lower()
        count = int(row.get("count", 0))

        if diff == "easy":
            easy = count
        elif diff == "medium":
            medium = count
        elif diff == "hard":
            hard = count
        elif diff == "all":
            solved_total = count

    # -------------------------
    # Contest data
    # -------------------------
    contest = data.get("data", {}).get("userContestRanking") or {}

    rating = contest.get("rating")
    contests = contest.get("attendedContestsCount")

    # safe defaults
    rating = int(rating) if rating else 1300
    contests = int(contests) if contests else 0

    return {
        "easy": easy,
        "medium": medium,
        "hard": hard,
        "solved": solved_total,
        "rating": rating,
        "contests": contests,
    }


# =========================================
# Sync Function
# =========================================
def sync_leetcode_by_username(user):

    account = PlatformAccount.objects.filter(
        user=user,
        platform__slug="leetcode"
    ).first()

    if not account:
        return None

    data = get_leetcode_stats(account.username)

    easy = data["easy"]
    medium = data["medium"]
    hard = data["hard"]
    solved = data["solved"]
    rating = data["rating"]
    contests = data["contests"]

    # ---------------------------------
    # XP FORMULA (difficulty + rating)
    # ---------------------------------
    rating_delta = max(0, rating - 1300)

    xp = (
        (easy * 5) +
        (medium * 10) +
        (hard * 20) +
        int((rating_delta ** 2) / 10) +
        (contests * 50)
    )

    stats, _ = UserStats.objects.get_or_create(user=user)

    # usernames
    stats.leetcode_username = account.username

    # counts
    stats.leetcode_easy = easy
    stats.leetcode_medium = medium
    stats.leetcode_hard = hard
    stats.leetcode_solved = solved

    # xp
    stats.leetcode_xp = xp

    stats.last_updated = timezone.now()
    stats.save()

    account.last_synced = timezone.now()
    account.save(update_fields=["last_synced"])

    # global recompute
    stats.recalculate_totals()

    return {
        "easy": easy,
        "medium": medium,
        "hard": hard,
        "solved": solved,
        "rating": rating,
        "contests": contests,
        "xp": xp
    }
