from playwright.sync_api import sync_playwright , expect

with sync_playwright() as p:
    browser = p.chromium.launch(headless = False)
    page = browser.new_page()
    page.goto("https://testautomationpractice.blogspot.com/p/playwrightpractice.html")
    
    def handel_dialog(dialog):
        print(dialog.type, dialog.message)
        print(dialog.default_value)
        dialog.accept("Pavandutt")
    #page.on("dialog", lambda dialog:dialog.accept())
    page.once("dialog", handel_dialog)
    page.locator('id=promptBtn').click()
    page.wait_for_timeout(3000)