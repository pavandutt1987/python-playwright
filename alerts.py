from playwright.sync_api import sync_playwright , expect
with sync_playwright() as p:    
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://testautomationpractice.blogspot.com/p/playwrightpractice.html")
    # def handel_dialog(dialog):
    #     print(f"Dialog message: {dialog.message}")
    #     dialog.accept()
    #page.on("dialog", handel_dialog)
    with page.expect_event("dialog") as dialog_info:
        page.locator("button[id='alertBtn']").click()
    dialog = dialog_info.value
    print(f"Dialog message: {dialog.message}")
    dialog.accept()
    # page.locator("button[id='alertBtn']").click()
    # page.wait_for_timeout(3000)

   
    
