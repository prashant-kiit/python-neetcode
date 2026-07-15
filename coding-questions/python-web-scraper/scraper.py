"""Scrape the 50 Python coding interview question titles from Internshala's blog.

Launches Chromium via Playwright, scrolls the page to trigger any lazily
loaded content, extracts the question titles in order, and writes them to
output/python_interview_questions.md.
"""

from __future__ import annotations

import logging
import re
import sys
from pathlib import Path

from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError, sync_playwright

URL = "https://internshala.com/blog/python-coding-interview-questions-and-answers/"
EXPECTED_QUESTION_COUNT = 50
QUESTION_SELECTOR = "div.entry-content h3.wp-block-heading"
QUESTION_PREFIX_RE = re.compile(r"^\s*Q\s*\d+\s*[.:)-]?\s*", re.IGNORECASE)
OUTPUT_PATH = Path(__file__).parent / "output" / "python_interview_questions.md"
NAVIGATION_TIMEOUT_MS = 60_000
SCROLL_PAUSE_MS = 1_000
MAX_SCROLL_ATTEMPTS = 30

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def load_page(page: Page, url: str) -> None:
    """Navigate to the target URL and wait for the page to settle."""
    logger.info("Navigating to %s", url)
    page.goto(url, wait_until="domcontentloaded", timeout=NAVIGATION_TIMEOUT_MS)
    page.wait_for_load_state("networkidle", timeout=NAVIGATION_TIMEOUT_MS)
    logger.info("Page loaded and network is idle")


def scroll_to_bottom(page: Page) -> None:
    """Repeatedly scroll to the bottom of the page until no new content loads."""
    logger.info("Scrolling to trigger any lazily loaded content")
    previous_height = 0
    for attempt in range(1, MAX_SCROLL_ATTEMPTS + 1):
        current_height = page.evaluate("document.body.scrollHeight")
        if current_height == previous_height:
            logger.info("Scroll height stable after %d attempt(s); stopping", attempt)
            break
        previous_height = current_height
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        try:
            page.wait_for_load_state("networkidle", timeout=SCROLL_PAUSE_MS)
        except PlaywrightTimeoutError:
            pass
        page.wait_for_timeout(SCROLL_PAUSE_MS)
    else:
        logger.warning("Reached max scroll attempts (%d) without a stable height", MAX_SCROLL_ATTEMPTS)


def wait_for_questions(page: Page, expected_count: int) -> None:
    """Wait until at least `expected_count` question headings are rendered."""
    logger.info("Waiting for at least %d question headings to render", expected_count)
    page.wait_for_function(
        """(args) => {
            const [selector, count] = args;
            return document.querySelectorAll(selector).length >= count;
        }""",
        arg=[QUESTION_SELECTOR, expected_count],
        timeout=NAVIGATION_TIMEOUT_MS,
    )


def extract_question_titles(page: Page) -> list[str]:
    """Extract question titles in document order, stripping the 'Qn.' prefix."""
    raw_titles = page.locator(QUESTION_SELECTOR).all_inner_texts()
    logger.info("Found %d raw heading candidates", len(raw_titles))

    titles: list[str] = []
    for raw in raw_titles:
        text = raw.strip()
        if not QUESTION_PREFIX_RE.match(text):
            continue
        cleaned = QUESTION_PREFIX_RE.sub("", text).strip()
        if cleaned:
            titles.append(cleaned)

    return deduplicate_preserve_order(titles)


def deduplicate_preserve_order(items: list[str]) -> list[str]:
    """Remove duplicates while preserving the first-seen order."""
    seen: set[str] = set()
    unique_items: list[str] = []
    for item in items:
        if item not in seen:
            seen.add(item)
            unique_items.append(item)
    return unique_items


def write_markdown(titles: list[str], output_path: Path) -> None:
    """Write the numbered question titles to a Markdown file."""
    logger.info("Writing %d question titles to %s", len(titles), output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    lines = ["# Python Coding Interview Questions", ""]
    lines.extend(f"{index}. {title}" for index, title in enumerate(titles, start=1))
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def scrape_question_titles(url: str, expected_count: int) -> list[str]:
    """Run the full scrape and return the extracted question titles."""
    with sync_playwright() as playwright:
        logger.info("Launching Chromium browser")
        browser = playwright.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            load_page(page, url)
            scroll_to_bottom(page)
            wait_for_questions(page, expected_count)
            return extract_question_titles(page)
        finally:
            browser.close()
            logger.info("Browser closed")


def main() -> int:
    try:
        titles = scrape_question_titles(URL, EXPECTED_QUESTION_COUNT)
    except PlaywrightTimeoutError:
        logger.error("Timed out waiting for the page or its content to load")
        return 1
    except Exception:
        logger.exception("Unexpected error while scraping")
        return 1

    if len(titles) != EXPECTED_QUESTION_COUNT:
        logger.error(
            "Expected %d question titles but found %d; aborting without writing output",
            EXPECTED_QUESTION_COUNT,
            len(titles),
        )
        return 1

    write_markdown(titles, OUTPUT_PATH)
    logger.info("Done. Output written to %s", OUTPUT_PATH)
    return 0


if __name__ == "__main__":
    sys.exit(main())
