import os
import re
import requests
from bs4 import BeautifulSoup
from django.utils import timezone
from core.models import PlatformAccount, UserStats

GITHUB_GRAPHQL = "https://api.github.com/graphql"
GITHUB_REST = "https://api.github.com"


def _first_int(text, default=0):
    match = re.search(r"\d+", text.replace(",", ""))
    return int(match.group(0)) if match else default


def scrape_github_profile(username):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; StudyStack/1.0)",
        "Accept": "text/html,application/xhtml+xml",
    }
    profile = requests.get(f"{GITHUB_REST.replace('api.', '')}/{username}", headers=headers, timeout=20)
    if profile.status_code == 404:
        raise Exception("GitHub user not found")
    profile.raise_for_status()

    soup = BeautifulSoup(profile.text, "lxml")
    text = soup.get_text("\n", strip=True)

    contributions = 0
    match = re.search(r"([\d,]+)\s+contributions?\s+in\s+the\s+last\s+year", text, re.I)
    if match:
        contributions = int(match.group(1).replace(",", ""))

    repos = 0
    repos_page = requests.get(
        f"{GITHUB_REST.replace('api.', '')}/{username}?tab=repositories",
        headers=headers,
        timeout=20,
    )
    repos_page.raise_for_status()
    repos_soup = BeautifulSoup(repos_page.text, "lxml")
    repo_counter = repos_soup.select_one('a[href$="?tab=repositories"] .Counter')
    if repo_counter:
        repos = _first_int(repo_counter.get_text(" ", strip=True))
    if not repos:
        repo_match = re.search(r"Repositories\s+([\d,]+)", repos_soup.get_text(" ", strip=True), re.I)
        repos = int(repo_match.group(1).replace(",", "")) if repo_match else 0

    return {
        "repos": repos,
        "contributions": contributions,
    }


# --------------------------------
# GraphQL — contributions
# --------------------------------
def get_contributions(username, token):
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

    r = requests.post(
        GITHUB_GRAPHQL,
        json={"query": query, "variables": {"login": username}},
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        timeout=15
    )
    r.raise_for_status()
    data = r.json()

    return (
        data["data"]["user"]["contributionsCollection"]
        ["contributionCalendar"]["totalContributions"]
    )


# --------------------------------
# Repo count (REST)
# --------------------------------
def get_repo_count(username, token=None):
    repos = []
    page = 1

    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"

    while True:
        r = requests.get(
            f"https://api.github.com/users/{username}/repos",
            params={"per_page": 100, "page": page},
            headers=headers,
            timeout=15
        )
        r.raise_for_status()
        data = r.json()

        if not data:
            break

        repos.extend(data)
        page += 1

    return len(repos)


# --------------------------------
# Main sync
# --------------------------------
def sync_github_activity(account):

    username = account.username
    token = os.getenv("GITHUB_TOKEN")  # ✅ auto-read env token

    repos = 0
    contributions = 0

    try:
        scraped = scrape_github_profile(username)
        repos = scraped["repos"]
        contributions = scraped["contributions"]
    except Exception as e:
        print("GitHub profile scrape failed:", e)

    if not repos:
        try:
            repos = get_repo_count(username)
        except Exception as e:
            print("GitHub repo fetch failed:", e)

    if not contributions and token:
        try:
            contributions = get_contributions(username, token)
        except Exception as e:
            print("GitHub contributions fetch failed:", e)

    # --------------------------------
    # YOUR FORMULA
    # (repos × 15) + (contributions × 5)
    # --------------------------------
    xp = (repos * 15) + (contributions * 5)

    stats, _ = UserStats.objects.get_or_create(user=account.user)

    stats.github_username = username
    stats.github_repos = repos
    stats.total_commits = contributions
    stats.github_xp = xp
    stats.last_updated = timezone.now()
    stats.save()

    # safe global recompute
    stats.recalculate_totals()

    account.last_synced = timezone.now()
    account.save(update_fields=["last_synced"])

    return {
        "repos": repos,
        "contributions": contributions,
        "xp": xp
    }
