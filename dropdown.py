from playwright.sync_api import sync_playwright , expect


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://rahulshettyacademy.com/AutomationPractice/")
    text = page.locator("#dropdown-class-example").text_content()
    print(text)
    page.locator("#dropdown-class-example").select_option("Option1")
    text = page.locator("#dropdown-class-example").input_value()
    page.wait_for_timeout(3000)
    print(text)

    
   