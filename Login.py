from playwright.sync_api import sync_playwright , expect
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.saucedemo.com/")
    print(page.title())
    expect(page).to_have_title("Swag Labs")

    userName = page.locator('[data-test="username"]')
    #userName.click()
    userName.fill("standard_user")
    password = page.get_by_placeholder("Password")
    #password.click()
    password.fill("secret_sauce")
    login =page.get_by_role("button", name="Login")
    login.click()
    page.wait_for_timeout(3000)
    #browser.close()