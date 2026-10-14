import json

from playwright.sync_api import Playwright , sync_playwright

def test_get_users(playwright: Playwright, url):
    # if we mention the url in the new_context() method then we don't need to mention the url in the get() method
    # request = playwright.request.new_context(base_url = url)
    request = playwright.request.new_context()
    # get will be used as response = request.get("")
    response = request.get(url)
    assert response.status == 200

    data = response.json()
    print(data)


 # Calling the method
if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_get_users(playwright,"https://jsonplaceholder.typicode.com/users")