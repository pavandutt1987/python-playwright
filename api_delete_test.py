import json
from playwright.sync_api import sync_playwright , Playwright

def test_delete_users(Playwright, url):
    request = Playwright.request.new_context(base_url = url , extra_http_headers = 
                                             {'x-api-key': 'free_user_3Kdk6cEvELwnqrrNCRSbhcTo1dk'})

    response = request.delete("")

    print(response.status)
    assert response.status == 204

if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_delete_users(playwright,"https://reqres.in/api/users/2")