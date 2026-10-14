import json
from playwright.sync_api import playwright, sync_playwright

def test_put_users(playwright,url):
    request = playwright.request.new_context(base_url = url , extra_http_headers = {'x-api-key': 'free_user_3Kdk6cEvELwnqrrNCRSbhcTo1dk'})

    payload = {
  "name": "morpheus",
  "job": "zion resident" }

    response = request.put("/2",data = payload)
    assert response.status == 200


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_put_users(playwright,"https://reqres.in/api/users")    
