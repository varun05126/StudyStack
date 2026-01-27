import requests
from datetime import date
from django.utils import timezone
from django.db.models import Sum

from core.models import DailyActivity, UserHeatmap, UserStats

GITHUB_API = "https://api.github.com"
XP_PER_COMMIT = 10


# ---------------------------------
# Public headers (no token needed)
# ---------------------------------
def github_headers():
    return {
        "Accept": "application/vnd.github+json",
        "User-Agent": "StudyStack-App"
    }


# ---------------------------------
# Fetch recent public events
# ---------------------------------
def fetch_events(username, per_page=100):
    url = f"{GITHUB_API}/users/{username}/events/public"
    r = requests.get(url, headers=github_headers(), params={"per_page": per_page}, timeout=15)
    r.raise_for_status()
    return r.json()


# ---------------------------------
# Main sync function
# ---------------------------------
def sync_github_activity(account):
    events = fetch_events(account.username)

    daily = {}

    for event in events:
        if event.get("type") != "PushEvent":
            continue

        day = event.get("created_at", "")[:10]
        commits = event.get("payload", {}).get("commits", [])

        if not commits:
            continue

        daily[day] = daily.get(day, 0) + len(commits)

    print("✅ GITHUB DAILY COMMITS:", daily)  # DEBUG

    # save daily activity
    for d, commits in daily.items():
        DailyActivity.objects.update_or_create(
            account=account,
            date=date.fromisoformat(d),
            defaults={
                "commits": commits,
                "xp": commits * XP_PER_COMMIT
            }
        )

    account.last_synced = timezone.now()
    account.save(update_fields=["last_synced"])

    update_user_heatmap(account.user)
    update_user_stats(account.user)


# ---------------------------------
# Heatmap
# ---------------------------------
def update_user_heatmap(user):
    qs = DailyActivity.objects.filter(account__user=user)

    heatmap = {}
    for act in qs:
        heatmap[act.date] = heatmap.get(act.date, 0) + act.xp

    for d, xp in heatmap.items():
        UserHeatmap.objects.update_or_create(
            user=user,
            date=d,
            defaults={
                "total_xp": xp,
                "activity_score": min(100, xp)
            }
        )


# ---------------------------------
# User stats
# ---------------------------------
def update_user_stats(user):
    qs = DailyActivity.objects.filter(account__user=user)

    total_commits = qs.aggregate(Sum("commits"))["commits__sum"] or 0
    github_xp = qs.aggregate(Sum("xp"))["xp__sum"] or 0

    stats, _ = UserStats.objects.get_or_create(user=user)

    stats.total_commits = total_commits
    stats.github_xp = github_xp

    stats.total_xp = (
        (stats.github_xp or 0) +
        (stats.leetcode_xp or 0) +
        (stats.gfg_xp or 0)
    )

    stats.level = max(1, stats.total_xp // 100)
    stats.last_updated = timezone.now()
    stats.save()
    