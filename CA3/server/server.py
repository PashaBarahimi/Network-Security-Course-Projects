import requests
import json

import uvicorn
from fastapi import FastAPI

CLIENT_ID = "ad4d6596591cda890604"
CLIENT_SECRET = "0b10c4851b977a26fbe6463ccffc63997f14ca1c"


app = FastAPI()


def get_access_token(code: str) -> str:
	access_token_url = "https://github.com/login/oauth/access_token"
	payload = {
		"client_id": CLIENT_ID,
		"client_secret": CLIENT_SECRET,
		"code": code
	}
	headers = {
		"Accept": "application/json"
	}
	response = requests.post(access_token_url, data=payload, headers=headers)
	access_token = response.json()['access_token']
	return access_token


def get_user_details(access_token: str) -> dict:
	api_url = "https://api.github.com/user"
	headers = {
		"Authorization": f"Bearer {access_token}"
	}
	response = requests.get(api_url, headers=headers)
	return response.json()


@app.get("/oauth/redirect")
def oauth_redirect(code: str) -> dict:
	access_token = get_access_token(code)
	user_details = get_user_details(access_token)
	print(f'Github code is: {code}')
	print(f'Github access token is: {access_token}')
	print(f'Github user details are: {json.dumps(user_details, indent=4)}')
	return user_details

if (__name__ == '__main__'):
	uvicorn.run(app, host= '0.0.0.0', port = 8589)
