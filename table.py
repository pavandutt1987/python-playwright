from playwright.sync_api import sync_playwright , expect
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://testautomationpractice.blogspot.com/p/playwrightpractice.html")

    links  = page.locator("//ul[@id='pagination']//li")
    print(links.count())
    for i in range(links.count()):
        links.nth(i).click()
        table = page.locator("//table[@id='productTable']//td").filter(has_text="Smartphone")