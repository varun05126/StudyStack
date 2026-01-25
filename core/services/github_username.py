import requests
from django.conf import settings
from django.utils import timezone
from core.models import UserStats

GITHUB_GRAPHQL = "https://api.github.com/graphql"

# -----------------------------
# CONFIG (easy to change later)
# -----------------------------
XP_PER_COMMIT = 10
XP_PER_LEVEL = 100


# --------------------------------
# Get total public GitHub contributions
# --------------------------------
def get_total_contributions(username: str) -> int:
    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
          }
        }
      }
    }
    """

    headers = {
        "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(
        GITHUB_GRAPHQL,
        json={"query": query, "variables": {"login": username}},
        headers=headers,
        timeout=20
    )

    if response.status_code != 200:
        raise Exception("GitHub API request failed")

    data = response.json()

    if "errors" in data:
        raise Exception(data["errors"])

    user = data.get("data", {}).get("user")
    if not user:
        return 0

    return user["contributionsCollection"]["contributionCalendar"]["totalContributions"]


# --------------------------------
# Main sync function
# --------------------------------
def sync_github_by_username(account):
    # 1. Fetch real total contributions
    total_commits = get_total_contributions(account.username)

    # 2. Get or create stats row
    stats, _ = UserStats.objects.get_or_create(user=account.user)

    # 3. Save commits
    stats.total_commits = total_commits

    # 4. XP SYSTEM (single source of truth)
    stats.total_xp = total_commits * XP_PER_COMMIT

    # 5. LEVEL SYSTEM
    stats.level = max(1, (stats.total_xp // XP_PER_LEVEL) + 1)

    # 6. Metadata
    stats.last_updated = timezone.now()
    stats.save()

    # 7. Update platform account
    account.last_synced = timezone.now()
    account.save()

    return total_commits
