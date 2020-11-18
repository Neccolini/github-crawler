import os 
from rauth import OAuth2Service
from requests_oauthlib import OAuth2Session
"""
(macなら) ~/.bash_profile に環境変数を追加しておく
"""
#GITHUB_CLIENT_ID=os.environ['GITHUB_CLIENT_ID']
#GITHUB_CLIENT_SECRET=os.environ["GITHUB_CLIENT_SECRET"]
if "GITHUB_ACCESS_TOKEN" not in os.environ:
    GITHUB_ACCESS_TOKEN=None
else:
    GITHUB_ACCESS_TOKEN=os.environ["GITHUB_ACCESS_TOKEN"]