import requests
from django.utils import timezone
from core.models import PlatformAccount, UserStats

def get_cf_stats(username: str):
    url = f"https://codeforces.com/api/user.status?handle={username}"
    r = requests.get(url, timeout=15)
    data = r.json()

    if data["status"] != "OK":
        raise Exception("Codeforces user not found")

    solved = set()
    for sub in data["result"]:
        if sub["verdict"] == "OK":
            solved.add(sub["problem"]["name"])

    return len(solved)


def sync_codeforces_by_username(user):
    account = PlatformAccount.objects.filter(
        user=user, platform__slug="codeforces"
    ).first()

    if not account:
        return None

    solved = get_cf_stats(account.username)
    xp = solved * 12

    stats, _ = UserStats.objects.get_or_create(user=user)

    stats.codeforces_solved = solved
    stats.codeforces_xp = xp

    stats.total_xp = (
        stats.total_commits * 10 +
        stats.leetcode_xp +
        stats.gfg_xp +
        stats.codeforces_xp
    )

    stats.level = max(1, stats.total_xp // 100 + 1)
    stats.last_updated = timezone.now()
    stats.save()

    account.last_synced = timezone.now()
    account.save()

    return solved