#!/usr/bin/python3

import time
import requests

host_path = "http://10.10.1.20:5000"
jwt_token = None

class ResponseFormatException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(f'Response Format Exception: {self.message}')

class RequestStatusException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(f'Request Status Exception: {self.message}')

def check_result(resp):
    if "result" not in resp:
        raise ResponseFormatException(f"response json must have 'result'")
    if resp["result"].lower() == 'ok':
        return True
    if resp["result"].lower() == 'fail':
        return False
    raise ResponseFormatException(f"response 'result' must be 'ok' or 'fail'")
    
''' /login '''

def request_login(url):
    post_headers = {
        "Content-Type": "application/json",
    }
    post_body = {
        "user": "Mike",
        "password": "123"
    }

    print(f"REQUEST => {url}")
    post_resp = requests.post(url, 
            headers = post_headers, 
            json = post_body)

    print(f"RESP => {post_resp.status_code}")
    if post_resp.status_code != 200:
        raise RequestStatusException(f"response status code: {post_resp.status_code}")

    resp = post_resp.json()

    print(f"RESP: ${resp}")

    if not check_result(resp):
        return

    jwt_token = resp["token"] 

''' /status '''

def request_status(url):
    post_headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {jwt_token}",
    }
    print(f"REQUEST => {url}")
    post_resp = requests.post(url, 
            headers = post_headers)

    print(f"RESP => {post_resp.status_code}")
    if post_resp.status_code != 200:
        raise RequestStatusException(f"response status code: {post_resp.status_code}")

    resp = post_resp.json()

    print(f"RESP: ${resp}")
    if not check_result(resp):
        return

def main():
    try:
        login_url = f"{host_path}/login"
        request_login(login_url)

        time.sleep(1)

        status_url = f"{host_path}/status"
        request_status(status_url)
    except Exception as e:
        print(f'+----------------------------------------+')
        print(f'| ERROR: {e}')
        print(f'+----------------------------------------+')

main()
