import json
from playwright.sync_api import playwright, sync_playwright

def test_post_users(playwright,url):
    request = playwright.request.new_context(base_url = url , extra_http_headers = {'x-api-key': 'free_user_3Kdk6cEvELwnqrrNCRSbhcTo1dk'})

    payload = {
  "name": "morpheus",
  "job": "leader"
}
    response = request.post("",data = payload)

    assert response.status == 201
    data = response.json()
    print(data)

    assert data['name'] == payload["name"]


if __name__ == "__main__":
    with sync_playwright() as playwright:
        test_post_users(playwright,"https://reqres.in/api/users")   