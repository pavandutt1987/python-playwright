from playwright.sync_api import sync_playwright , Playwright

def run(playwright : Playwright):
    webkit =playwright.webkit
    chromium = playwright.chromium.launch(headless = False)
    #iphone = playwright.devices['iPhone 13 Pro']
    android = playwright.devices['Pixel 5']
    #browser = chromium.launch(headless = False)
    context = chromium.new_context(**android)

    #browser = webkit.launch(headless = False)
    #context = browser.new_context(**iphone)
    page = context.new_page()
    page.goto("https://q1espn-ms.qa1blue.ccvapor.net/account/index.html")
    page.wait_for_timeout(60000)
    text = page.title()
    print(text)
    page.close()

if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
