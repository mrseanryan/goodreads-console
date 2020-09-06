#! python3
"""
Add a book to to 'to read' shelf.

Requires OAuth authorization (via 'grc-authorize.py')
"""

import pdb
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


def get_oath_token():
    return read_file("oath.token.credentials.txt")


def get_oath_token_secret():
    return read_file("oath.token-secret.credentials.txt")


new_session = OAuth1Session(
    consumer_key=get_dev_key(),
    consumer_secret=get_dev_secret(),
    access_token=get_oath_token(),
    access_token_secret=get_oath_token_secret()
)

# TODO xxx add a 'find book id' command

# xxx add a book - WORKS!
# book_id 631932 is "The Greedy Python"
data = {'name': 'to-read', 'book_id': 631932}

# # add this to our "to-read" shelf
response = new_session.post(
    'https://www.goodreads.com/shelf/add_to_shelf.xml', data)

if response.status_code != 201:
    raise Exception('Cannot create resource: %s' % response.status_code)
else:
    print('Book added!')
