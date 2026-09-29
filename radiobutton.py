from playwright.sync_api import sync_playwright , expect
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://testautomationpractice.blogspot.com/p/playwrightpractice.html")
    print(page.title())
    page.get_by_label("Standard").click()
    page.wait_for_timeout(3000)
    assert page.get_by_label("Standard").is_checked() == True
    assert page.get_by_label("Express").is_checked() == False
    page.get_by_label("Express").click()
    page.wait_for_timeout(3000)
    checked= page.get_by_label("Standard").is_checked() == False
    print(checked)