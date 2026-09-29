import asyncio
from playwright.async_api import  async_playwright

async def page_title(browser,url):
    context = await browser.new_context()
    page = await context.new_page()
    await page.goto(url)
    title = await page.title()
    print(f"Title of {url} is: {title}")
    context.close()


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        browser1 = await p.firefox.launch(headless=False)
        urls = ["https://testautomationpractice.blogspot.com/p/playwrightpractice.html",
                "https://www.google.com/",
                "https://www.youtube.com/"]
        #tasks = [page_title(browser, url) for url in urls]
        #await asyncio.gather(*tasks)
        await asyncio.gather(page_title(browser,"https://testautomationpractice.blogspot.com/p/playwrightpractice.html"),
                             page_title(browser1,"https://www.google.com/"))
        await browser.close()
asyncio.run(main())