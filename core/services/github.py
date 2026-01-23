import requests
from datetime import date
from django.utils import timezone
from django.db.models import Sum

from core.models import DailyActivity, UserHeatmap, UserStats

GITHUB_API = "https://api.github.com"


# =====================================
# HEADERS
# =====================================

def github_headers(account):
    return {
        "Authorization": f"token {account.access_token}",
        "Accept": "application/vnd.github+json"
    }


# =====================================
# FETCH EVENTS
# =====================================

def fetch_events(account, per_page=100):
    """
    Fetch recent public GitHub events for a user.
    """
    r = requests.get(
        f"{GITHUB_API}/users/{account.username}/events",
        headers=github_headers(account),
        params={"per_page": per_page},
        timeout=15
    )
    r.raise_for_status()
    return r.json()


# =====================================
# SYNC ENGINE
# =====================================

def sync_github_activity(account):
    """
    Main sync function.
    Converts GitHub PushEvents into daily commit counts.
    """
    events = fetch_events(account)
    daily = {}

    for event in events:
        if event.get("type") != "PushEvent":
            continue

        day = event.get("created_at", "")[:10]
        commits = event.get("payload", {}).get("commits", [])

        commit_count = len(commits)
        if commit_count == 0:
            continue

        daily[day] = daily.get(day, 0) + commit_count

    # Save daily activity
    for d, commits in daily.items():
        d = date.fromisoformat(d)

        DailyActivity.objects.update_or_create(
            account=account,
            date=d,
            defaults={
                "commits": commits,
                "xp": commits * 5
            }
        )

    # Mark sync time
    account.last_synced = timezone.now()
    account.save(update_fields=["last_synced"])

    # Update aggregates
    update_user_heatmap(account.user)
    update_user_stats(account.user)


# =====================================
# HEATMAP AGGREGATION
# =====================================

def update_user_heatmap(user):
    """
    Builds per-day XP heatmap across all platforms.
    """
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


# =====================================
# USER STATS AGGREGATION
# =====================================

def update_user_stats(user):
    """
    Updates total commits, XP and level.
    """
    qs = DailyActivity.objects.filter(account__user=user)

    total_commits = qs.aggregate(Sum("commits"))["commits__sum"] or 0
    total_xp = qs.aggregate(Sum("xp"))["xp__sum"] or 0

    stats, _ = UserStats.objects.get_or_create(user=user)

    stats.total_commits = total_commits
    stats.total_xp = total_xp
    stats.level = max(1, total_xp // 500)
    stats.save()
    