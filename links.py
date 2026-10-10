from playwright.sync_api import sync_playwright , expect
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://testautomationpractice.blogspot.com/p/playwrightpractice.html")
    links = page.locator("a")
    for i in range (links.count()):
        print(links.nth(i).get_attribute("href"))
    page.wait_for_timeout(3000)
    # slider = page.locator("//div[@class='ui-slider-handle ui-corner-all ui-state-default']")
    # page.wait_for_timeout(3000)
    # slider_handle = slider.nth(0)
    # slider_handle.drag_to(slider_handle, source_position=(0, 0), target_position=(100, 0))
    with page.expect_file_chooser() as file_chooser:
        page.locator("id=singleFileInput").click()
    file_info = file_chooser.value
    file_info.set_files("E:/infosys.txt")
    page.screenshot(path="E:/screenshot.png")