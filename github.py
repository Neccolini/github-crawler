import os 
from rauth import OAuth2Service
from requests_oauthlib import OAuth2Session
"""
環境変数を追加しておく
"""
GITHUB_CLIENT_ID=os.environ['GITHUB_CLIENT_ID']
GITHUB_CLIENT_SECRET=os.environ["GITHUB_CLIENT_SECRET"]
GITHUB_ACCESS_TOKEN=os.environ["GITHUB_ACCESS_TOKEN"]
authorization_base_url = "https://github.com/login/oauth/authorize?user%20gist"
token_url="https://github.com/login/oauth/access_token"
github = OAuth2Session(GITHUB_CLIENT_ID)
authorization_url, state = github.authorization_url(authorization_base_url)
print("Please go here and authorize,", authorization_url)
redirect_response="https://github.com/Neccolini/github-crawler"