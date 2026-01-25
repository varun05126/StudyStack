import requests
from django.utils import timezone
from core.models import UserStats

LEETCODE_API = "https://leetcode-stats-api.herokuapp.com"

XP_EASY = 5
XP_MEDIUM = 10
XP_HARD = 20


def get_leetcode_stats(username: str):
    url = f"{LEETCODE_API}/{username}"
    r = requests.get(url, timeout=15)

    if r.status_code != 200:
        raise Exception("LeetCode user not found")

    data = r.json()

    if data.get("status") != "success":
        raise Exception("Invalid LeetCode username")

    return {
        "total": data.get("totalSolved", 0),
        "easy": data.get("easySolved", 0),
        "medium": data.get("mediumSolved", 0),
        "hard": data.get("hardSolved", 0),
    }


def sync_leetcode_by_username(user, username: str):
    stats_data = get_leetcode_stats(username)

    easy = stats_data["easy"]
    medium = stats_data["medium"]
    hard = stats_data["hard"]

    leetcode_xp = (easy * XP_EASY) + (medium * XP_MEDIUM) + (hard * XP_HARD)

    stats, _ = UserStats.objects.get_or_create(user=user)

    # Store leetcode-specific fields if you add them later
    stats.leetcode_solved = stats_data["total"]
    stats.leetcode_xp = leetcode_xp

    # For now, just add into total_xp
    stats.total_xp = leetcode_xp
    stats.last_updated = timezone.now()
    stats.save()

    return stats_data, leetcode_xp
