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
        profile {
          ranking
        }
        contestBadge {
          name
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
    # solved counts
    # -------------------------
    solved_data = user["submitStatsGlobal"]["acSubmissionNum"]

    solved_total = 0
    for row in solved_data:
        if row["difficulty"].lower() == "all":
            solved_total = row["count"]

    # -------------------------
    # contest data
    # -------------------------
    contest = data.get("data", {}).get("userContestRanking") or {}
    rating = contest.get("rating") or 1300
    contests = contest.get("attendedContestsCount") or 0

    return {
        "solved": solved_total,
        "rating": int(rating),
        "contests": int(contests),
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

    solved = data["solved"]
    rating = data["rating"]
    contests = data["contests"]

    # ---------------------------------
    # XP FORMULA (your rule)
    # ---------------------------------
    xp = (
        (solved * 10)
        + int(((rating - 1300) ** 2) / 10)
        + (contests * 50)
    )

    stats, _ = UserStats.objects.get_or_create(user=user)

    stats.leetcode_username = account.username
    stats.leetcode_solved = solved
    stats.leetcode_xp = xp
    stats.last_updated = timezone.now()
    stats.save()

    account.last_synced = timezone.now()
    account.save(update_fields=["last_synced"])

    # safe global recalc
    stats.recalculate_totals()

    return {
        "solved": solved,
        "rating": rating,
        "contests": contests,
        "xp": xp
    }