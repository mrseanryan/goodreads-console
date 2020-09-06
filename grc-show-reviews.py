#! python3
"""
Retrieve reviews that the user has written.
"""

import pdb
import requests
import xmltodict

import goodreads_api_client as gr


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


# https://www.goodreads.com/api/index#reviews.list
resp = requests.get('https://www.goodreads.com/review/list/'+get_user_id()+'.xml',
                    params={'key': get_dev_key(), 'v': 2, 'id': get_user_id(), 'sort': 'review'})
# TODO - request by page (1.1 second delay between requests)
# until hit a book that has no review

data_dict = xmltodict.parse(resp.content)['GoodreadsResponse']
reviews_books = [r for r in data_dict['reviews']['review']]


def print_review(review):
    reduced_review = {'link': review['link'], 'body': review['body'],
                      'read_count': review['read_count'],
                      'date_added': review['date_added'],
                      'date_updated': review['date_updated']
                      # TODO add rating
                      }
    print(reduced_review)


list(map(lambda x: print_review(x), reviews_books))

# TODO - output in CSV format
