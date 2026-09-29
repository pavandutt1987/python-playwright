from playwright.sync_api import sync_playwright , expect

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://rahulshettyacademy.com/AutomationPractice/")
    page.locator("input[name='checkBoxOption1']").check()
    page.wait_for_timeout(3000)
    assert page.locator("input[name='checkBoxOption1']").is_checked() == True
    page.locator("input[name='checkBoxOption1']").uncheck()
    page2= browser.new_page()
    page2.goto("https://testautomationpractice.blogspot.com/p/playwrightpractice.html#")
    page2.get_by_role("button",name="Primary Action").click()
    page2.get_by_role("checkbox",name = " Accept terms").check()
    page2.wait_for_timeout(3000)