#! python3
"""
Perform OAuth authentication - requires user approval.

Session tokens are saved for later use (they are valid, until the user revokes access).
"""

import requests
import xmltodict

import goodreads_api_client as gr
from rauth.service import OAuth1Service, OAuth1Session


def read_file(filename):
    f = open(filename, "r")
    return f.read()


def get_dev_key():
    return read_file("key.credentials.txt")


def get_dev_secret():
    return read_file("secret.credentials.txt")


def get_user_id():
    return read_file("user-id.credentials.txt")


goodreads = OAuth1Service(
    consumer_key=get_dev_key(),
    consumer_secret=get_dev_secret(),
    name='goodreads',
    request_token_url='https://www.goodreads.com/oauth/request_token',
    authorize_url='https://www.goodreads.com/oauth/authorize',
    access_token_url='https://www.goodreads.com/oauth/access_token',
    base_url='https://www.goodreads.com/'
)

# head_auth=True is important here; this doesn't work with oauth2 for some reason
request_token, request_token_secret = goodreads.get_request_token(
    header_auth=True)

authorize_url = goodreads.get_authorize_url(request_token)
print('Visit this URL in your browser: ' + authorize_url)
accepted = 'n'
while accepted.lower() == 'n':
    # you need to access the authorize_link via a browser,
    # and proceed to manually authorize the consumer
    accepted = input('Have you authorized me? (y/n) ')

session = goodreads.get_auth_session(request_token, request_token_secret)
ACCESS_TOKEN = session.access_token
ACCESS_TOKEN_SECRET = session.access_token_secret

f = open("oath.token.credentials.txt", "a")
f.write(ACCESS_TOKEN)
f.close()

f = open("oath.token-secret.credentials.txt", "a")
f.write(ACCESS_TOKEN_SECRET)
f.close()

print("Authorization tokens saved for use")
