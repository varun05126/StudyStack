import requests
from datetime import date, timedelta
from django.utils import timezone
from django.db.models import Sum

from core.models import DailyActivity, UserHeatmap, UserStats

GITHUB_API = "https://api.github.com"


def github_headers(account):
    return {
        "Authorization": f"Bearer {account.access_token}",
        "Accept": "application/vnd.github+json"
    }


# -----------------------------------
# REAL COMMIT COUNTER (SEARCH API)
# -----------------------------------

def fetch_commit_count(username, token, day):
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    start = day.isoformat()
    end = (day + timedelta(days=1)).isoformat()

    q = f"author:{username} committer-date:{start}..{end}"

    r = requests.get(
        f"{GITHUB_API}/search/commits",
        headers=headers,
        params={"q": q}
    )

    if r.status_code != 200:
        return 0

    return r.json().get("total_count", 0)


# -----------------------------------
# MAIN SYNC ENGINE
# -----------------------------------

def sync_github_activity(account, days=30):
    today = date.today()

    for i in range(days):
        day = today - timedelta(days=i)

        commit_count = fetch_commit_count(
            account.username,
            account.access_token,
            day
        )

        DailyActivity.objects.update_or_create(
            account=account,
            date=day,
            defaults={
                "commits": commit_count,
                "xp": commit_count * 5
            }
        )

    account.last_synced = timezone.now()
    account.save(update_fields=["last_synced"])

    update_user_heatmap(account.user)
    update_user_stats(account.user)


# -----------------------------------
# AGGREGATIONS
# -----------------------------------

def update_user_heatmap(user):
    qs = DailyActivity.objects.filter(account__user=user)

    heatmap = {}
    for act in qs:
        heatmap.setdefault(act.date, 0)
        heatmap[act.date] += act.xp

    for d, xp in heatmap.items():
        UserHeatmap.objects.update_or_create(
            user=user,
            date=d,
            defaults={
                "total_xp": xp,
                "activity_score": min(100, xp)
            }
        )


def update_user_stats(user):
    qs = DailyActivity.objects.filter(account__user=user)

    total_commits = qs.aggregate(Sum("commits"))["commits__sum"] or 0
    total_xp = qs.aggregate(Sum("xp"))["xp__sum"] or 0

    stats, _ = UserStats.objects.get_or_create(user=user)

    stats.total_commits = total_commits
    stats.total_xp = total_xp
    stats.level = max(1, total_xp // 500)
    stats.save()