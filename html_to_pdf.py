#!/home/greggsoft/develop/greggsoft/greggsoft.github.io/venv/bin/python
"""
Convert an HTML file to PDF using Playwright/Chromium.

Install:
    pip install playwright
    playwright install chromium

Usage:
    ./venv/bin/python html_to_pdf.py resume.html resume.pdf
"""

import argparse
import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright


CHROMIUM_PATHS = (
    os.environ.get("CHROMIUM_PATH"),
    "/usr/bin/chromium",
    "/usr/bin/chromium-browser",
)


async def convert(input_html: str, output_pdf: str) -> None:
    html_file = Path(input_html).resolve()
    pdf_file = Path(output_pdf).resolve()

    if not html_file.exists():
        raise FileNotFoundError(f"HTML file not found: {html_file}")

    pdf_file.parent.mkdir(parents=True, exist_ok=True)

    chromium_path = next((path for path in CHROMIUM_PATHS if path and Path(path).exists()), None)
    if chromium_path is None:
        raise RuntimeError(
            "Chromium не найден. Укажите путь через CHROMIUM_PATH или установите Chromium."
        )

    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=chromium_path)
        page = await browser.new_page()
        await page.goto(html_file.as_uri(), wait_until="networkidle")

        await page.pdf(
            path=str(pdf_file),
            format="A4",
            print_background=True,
            prefer_css_page_size=True,
            margin={
                "top": "0",
                "right": "0",
                "bottom": "0",
                "left": "0",
            },
        )

        await browser.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert HTML to PDF")
    parser.add_argument("input_html", help="Input HTML file")
    parser.add_argument("output_pdf", help="Output PDF file")
    args = parser.parse_args()

    asyncio.run(convert(args.input_html, args.output_pdf))
    print(f"Created: {Path(args.output_pdf).resolve()}")


if __name__ == "__main__":
    main()
