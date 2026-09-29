from playwright.sync_api import sync_playwright , expect

def get_page_title(browser,url):
    context = browser.new_context()
    page = context.new_page()
    page.goto(url)
    title = page.title()
    print(f"Title of {url} is: {title}")
    context.close()




def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        urls = ["https://testautomationpractice.blogspot.com/p/playwrightpractice.html",
                "https://www.google.com/",
                "https://www.youtube.com/"]
        for url in urls:
            get_page_title(browser, url)
        browser.close()

main()
