# Python Web Scraper — Internshala Interview Questions

Scrapes the 50 Python coding interview question titles from Internshala's blog
using Playwright (Chromium) and writes them to a numbered Markdown file.

Target page:
https://internshala.com/blog/python-coding-interview-questions-and-answers/

## Project structure

```text
python-web-scraper/
├── venv/
├── scraper.py
├── requirements.txt
├── output/
│   └── python_interview_questions.md
└── README.md
```

## Requirements

- Python 3.12+
- macOS/Linux/Windows with internet access

## Setup

1. Create and activate a virtual environment:

   ```bash
   python3 -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Install the Chromium browser binary used by Playwright:

   ```bash
   playwright install chromium
   ```

## Running the scraper

```bash
python scraper.py
```

The script will:

1. Launch headless Chromium.
2. Navigate to the target page and wait for it to fully load.
3. Scroll to the bottom repeatedly until no more content loads.
4. Wait for all 50 question headings to be present in the DOM.
5. Extract the question titles in order, strip the `Qn.` prefix, and
   de-duplicate them while preserving order.
6. Write the result to `output/python_interview_questions.md`.

If fewer than 50 unique question titles are found, the script logs an error
and exits with a non-zero status without writing the output file — it will
not produce a partial/incorrect result.

## Output format

`output/python_interview_questions.md`:

```markdown
# Python Coding Interview Questions

1. Question title
2. Question title
...
50. Question title
```

## Notes

- Selectors are scoped to `div.entry-content h3.wp-block-heading` and
  filtered by a `Qn.` prefix regex, which excludes navigation, ads, related
  posts, comments, and footer content.
- If Internshala changes their page markup, update `QUESTION_SELECTOR` and
  `QUESTION_PREFIX_RE` in `scraper.py`.
