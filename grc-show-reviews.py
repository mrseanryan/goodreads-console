#! python3
"""
Retrieve reviews that the user has written.
"""

import pdb
import requests
import xmltodict
import time


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


def print_review(review):
    reduced_review = {'link': review['link'], 'body': review['body'],
                      'read_count': review['read_count'],
                      'date_added': review['date_added'],
                      'date_updated': review['date_updated']
                      # TODO add rating
                      }
    print(reduced_review)


def has_review_a_body(review):
    return not has_review_no_body(review)


def has_review_no_body(review):
    return review['body'] is None


has_review = True
page = 1

while has_review:
    # https://www.goodreads.com/api/index#reviews.list
    resp = requests.get('https://www.goodreads.com/review/list/'+get_user_id()+'.xml',
                        params={'key': get_dev_key(), 'v': 2, 'id': get_user_id(), 'sort': 'review', 'page': page})

    data_dict = xmltodict.parse(resp.content)['GoodreadsResponse']
    book_reviews = [r for r in data_dict['reviews']['review']]

    book_reviews_filtered = list(filter(has_review_a_body, book_reviews))

    list(map(lambda x: print_review(x), book_reviews_filtered))

    # until hit a book that has no review
    book_reviews_no_body = list(filter(has_review_no_body, book_reviews))
    if any(book_reviews_no_body):
        has_review = False
    else:
        page = page + 1
        # 1.1 second delay between requests, to meet quota
        time.sleep(1.1)


# TODO - output in CSV format
