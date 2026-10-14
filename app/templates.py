from typing import Dict, List, Any

TEMPLATES: Dict[str, Dict[str, Any]] = {
    "blank": {
        "title": "Blank Editor (Empty)",
        "description": "Clean empty editor for writing and running your own Playwright code.",
        "python": "",
        "typescript": "",
        "javascript": ""
    },
    "headed_demo": {
        "title": "Live Browser Demo",
        "description": "Open the built-in playground and keep the browser visible for 15 seconds.",
        "python": '''import asyncio
import os
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=os.environ.get("HEADED") != "1")
        page = await browser.new_page()
        await page.goto("http://127.0.0.1:8000/playground/login.html")
        print("Browser ready. Inspect it in the live browser panel.")
        await page.wait_for_timeout(15000)
        await browser.close()

asyncio.run(main())
''',
        "javascript": '''const { chromium } = require('playwright');

(async () => {
    const browser = await chromium.launch({ headless: process.env.HEADED !== '1' });
    const page = await browser.newPage();
    await page.goto('http://127.0.0.1:8000/playground/login.html');
    console.log('Browser ready. Inspect it in the live browser panel.');
    await page.waitForTimeout(15000);
    await browser.close();
})();
''',
        "typescript": '''import { chromium } from 'playwright';

(async () => {
    const browser = await chromium.launch({ headless: process.env.HEADED !== '1' });
    const page = await browser.newPage();
    await page.goto('http://127.0.0.1:8000/playground/login.html');
    console.log('Browser ready. Inspect it in the live browser panel.');
    await page.waitForTimeout(15000);
    await browser.close();
})();
''',
    }
}

def get_template_list() -> List[Dict[str, str]]:
    return [
        {
            "id": k,
            "title": v["title"],
            "description": v["description"]
        }
        for k, v in TEMPLATES.items()
    ]

def get_template_code(template_id: str, language: str) -> str:
    return TEMPLATES.get(template_id, {}).get(language, "")
