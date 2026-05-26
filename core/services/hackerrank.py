import requests
from django.utils import timezone
from core.models import PlatformAccount, UserStats

def get_hr_solved(username: str):
    url = f"https://www.hackerrank.com/rest/hackers/{username}/profile"
    r = requests.get(url, timeout=15)
    data = r.json()

    return data["model"]["solved_challenges"]


def sync_hackerrank_by_username(user):
    account = PlatformAccount.objects.filter(
        user=user, platform__slug="hackerrank"
    ).first()

    if not account:
        return None

    solved = get_hr_solved(account.username)
    xp = solved * 6

    stats, _ = UserStats.objects.get_or_create(user=user)

    stats.hackerrank_solved = solved
    stats.hackerrank_xp = xp

    stats.total_xp = (
        stats.total_commits * 10 +
        stats.leetcode_xp +
        stats.gfg_xp +
        stats.codeforces_xp +
        stats.hackerrank_xp
    )

    stats.level = max(1, stats.total_xp // 100 + 1)
    stats.last_updated = timezone.now()
    stats.save()

    account.last_synced = timezone.now()
    account.save()

    return solved