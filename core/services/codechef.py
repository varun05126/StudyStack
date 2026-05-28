import re

import requests
from bs4 import BeautifulSoup
from django.utils import timezone

from core.models import PlatformAccount, UserStats


CODECHEF_PROFILE_URL = "https://www.codechef.com/users/{username}"


def _first_int(value, default=0):
    match = re.search(r"\d+", value.replace(",", ""))
    return int(match.group(0)) if match else default


def get_codechef_stats(username: str):
    url = CODECHEF_PROFILE_URL.format(username=username)
    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; StudyStack/1.0)",
            "Accept": "text/html,application/xhtml+xml",
        },
        timeout=20,
    )

    if response.status_code == 404:
        raise Exception("CodeChef user not found")
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "lxml")
    page_text = soup.get_text("\n", strip=True)

    rating_node = soup.select_one(".rating-number")
    rating = _first_int(rating_node.get_text(" ", strip=True), 0) if rating_node else 0

    contests = 0
    html_contests = re.search(r"Contests\s*\((\d+)\)", response.text, re.I)
    if html_contests:
        contests = int(html_contests.group(1))
    contests_node = soup.find(string=re.compile(r"Contest Participated|Contests", re.I))
    if not contests and contests_node:
        parent_text = contests_node.parent.get_text(" ", strip=True) if contests_node.parent else str(contests_node)
        contests = _first_int(parent_text, 0)
    if not contests:
        match = re.search(r"Contests\s*\(?\s*(\d+)\s*\)?", page_text, re.I)
        contests = int(match.group(1)) if match else 0

    solved = 0
    solved_heading = soup.find(string=re.compile(r"Fully Solved|Total Problems Solved|Problems Solved", re.I))
    if solved_heading:
        section_text = solved_heading.parent.get_text(" ", strip=True) if solved_heading.parent else str(solved_heading)
        solved = _first_int(section_text, 0)

    if not solved:
        match = re.search(r"(?:Fully Solved|Total Problems Solved|Problems Solved)\s*:?\s*\(?\s*(\d+)\s*\)?", page_text, re.I)
        solved = int(match.group(1)) if match else 0

    rating_bonus = max(0, rating - 1200)
    xp = (solved * 2) + rating_bonus + (contests * 25)

    return {
        "solved": solved,
        "rating": rating,
        "contests": contests,
        "xp": xp,
    }


def sync_codechef_by_username(user):
    account = PlatformAccount.objects.filter(
        user=user,
        platform__slug="codechef",
    ).first()

    if not account:
        return None

    data = get_codechef_stats(account.username)
    stats, _ = UserStats.objects.get_or_create(user=user)

    stats.codechef_username = account.username
    stats.codechef_solved = data["solved"]
    stats.codechef_rating = data["rating"]
    stats.codechef_contests = data["contests"]
    stats.codechef_xp = data["xp"]
    stats.last_updated = timezone.now()
    stats.save(update_fields=[
        "codechef_username",
        "codechef_solved",
        "codechef_rating",
        "codechef_contests",
        "codechef_xp",
        "last_updated",
    ])

    account.last_synced = timezone.now()
    account.save(update_fields=["last_synced"])
    stats.recalculate_totals()

    return data
