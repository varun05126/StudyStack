from playwright.sync_api import sync_playwright
from django.utils import timezone
from core.models import PlatformAccount, UserStats

XP_PER_PROBLEM = 8


def get_gfg_stats(username: str):
    url = f"https://www.geeksforgeeks.org/profile/{username}/?tab=activity"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, timeout=60000)
        page.wait_for_timeout(8000)

        content = page.inner_text("body")
        browser.close()

    lines = [l.strip() for l in content.split("\n") if l.strip()]

    solved = 0
    score = 0

    for i, line in enumerate(lines):
        if line.lower() == "problems solved":
            solved = int("".join(c for c in lines[i+1] if c.isdigit()) or 0)

        if line.lower() == "coding score":
            score = int("".join(c for c in lines[i+1] if c.isdigit()) or 0)

    return {
        "solved": solved,
        "score": score
    }


def sync_gfg_by_username(user):

    account = PlatformAccount.objects.filter(
        user=user, platform__slug="gfg"
    ).first()

    if not account:
        return None

    data = get_gfg_stats(account.username)

    solved = data["solved"]
    score = data["score"]

    stats, _ = UserStats.objects.get_or_create(user=user)

    stats.gfg_solved = solved
    stats.gfg_xp = solved * XP_PER_PROBLEM
    stats.last_updated = timezone.now()
    stats.save()

    account.last_synced = timezone.now()
    account.save(update_fields=["last_synced"])

    return solved
