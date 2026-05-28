import json
import re

import requests
from bs4 import BeautifulSoup
from django.utils import timezone

from core.models import PlatformAccount, UserStats


HACKERRANK_PROFILE_URL = "https://www.hackerrank.com/profile/{username}"
HACKERRANK_PROFILE_API = "https://www.hackerrank.com/rest/hackers/{username}/profile"


def _solved_from_html(html: str):
    soup = BeautifulSoup(html, "lxml")

    next_data = soup.select_one("script#__NEXT_DATA__")
    if next_data and next_data.string:
        try:
            payload = json.loads(next_data.string)
            text = json.dumps(payload)
            match = re.search(r'"solved_challenges"\s*:\s*(\d+)', text)
            if match:
                return int(match.group(1))
        except json.JSONDecodeError:
            pass

    text = soup.get_text(" ", strip=True)
    patterns = [
        r"solved challenges?\s*(\d+)",
        r"challenges solved\s*(\d+)",
        r"(\d+)\s*challenges solved",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.I)
        if match:
            return int(match.group(1))

    return None


def get_hackerrank_stats(username: str):
    response = requests.get(
        HACKERRANK_PROFILE_URL.format(username=username),
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; StudyStack/1.0)",
            "Accept": "text/html,application/xhtml+xml",
        },
        timeout=20,
    )

    solved = None
    if response.status_code == 200:
        solved = _solved_from_html(response.text)
    elif response.status_code == 404:
        raise Exception("HackerRank user not found")
    else:
        response.raise_for_status()

    if solved is None:
        api_response = requests.get(
            HACKERRANK_PROFILE_API.format(username=username),
            headers={"User-Agent": "Mozilla/5.0 (compatible; StudyStack/1.0)"},
            timeout=20,
        )
        if api_response.status_code == 404:
            raise Exception("HackerRank user not found")
        api_response.raise_for_status()
        solved = int(api_response.json().get("model", {}).get("solved_challenges") or 0)

    xp = solved * 6
    return {
        "solved": solved,
        "xp": xp,
    }


def sync_hackerrank_by_username(user):
    account = PlatformAccount.objects.filter(
        user=user,
        platform__slug="hackerrank",
    ).first()

    if not account:
        return None

    data = get_hackerrank_stats(account.username)
    stats, _ = UserStats.objects.get_or_create(user=user)

    stats.hackerrank_username = account.username
    stats.hackerrank_solved = data["solved"]
    stats.hackerrank_xp = data["xp"]
    stats.last_updated = timezone.now()
    stats.save(update_fields=[
        "hackerrank_username",
        "hackerrank_solved",
        "hackerrank_xp",
        "last_updated",
    ])

    account.last_synced = timezone.now()
    account.save(update_fields=["last_synced"])
    stats.recalculate_totals()

    return data
