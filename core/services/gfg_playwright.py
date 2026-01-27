from playwright.sync_api import sync_playwright
import re


def get_gfg_stats(username: str):
    url = f"https://www.geeksforgeeks.org/profile/{username}?tab=activity"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)   # headless=True for server
        page = browser.new_page()
        page.goto(url, timeout=60000)

        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(8000)  # allow JS to fully render

        text = page.inner_text("body")

        browser.close()

    # -----------------------------
    # Extract numbers using regex
    # -----------------------------
    solved = 0
    score = 0

    solved_match = re.search(r"Problems Solved\s+(\d+)", text)
    score_match = re.search(r"Coding Score\s+(\d+)", text)

    if solved_match:
        solved = int(solved_match.group(1))

    if score_match:
        score = int(score_match.group(1))

    return {
        "solved": solved,
        "score": score
    }
