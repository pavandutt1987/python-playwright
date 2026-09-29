from playwright.sync_api import sync_playwright , expect
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://testautomationpractice.blogspot.com/p/playwrightpractice.html")
    links = page.locator("a")
    for i in range (links.count()):
        print(links.nth(i).get_attribute("href"))
    