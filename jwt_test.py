#!/usr/bin/python3

import requests

def http_post(url, data):
    post_resp = requests.post(url, json = data)
    post_resp_json = post_resp.json()
    return post_resp_json

def request_login(url):
    post_body = {
        "user": "Mike",
        "password": "123"
    }
    print("send request to %s\n" % (url,))
    resp = http_post(url, post_body)
    print("get response: %s\n" % resp)

login_url = "http://10.10.1.20:5000/login"
request_login(login_url)
