#! python3
"""
Retrieve reviews that the user has written.
"""

from dateutil.parser import parse
import pdb
import requests
import time
import xmltodict

# A character that is unlikely to appear inside a book review text.
CSV_SEPARATOR = "_"


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


def parse_date(date_time_str):
    # Date is like:
    # 'Sat Jun 27 04:16:51 -0700 2020'
    return parse(date_time_str)


def reduce_review(review):
    # TODO refactor via 'select' or 'map'
    return {
        'title': review['book']['title'],
        # TODO isbn: need to lookup and convert to a real ISBN (some books do not have one!)
        'isbn-id': review['book']['isbn'],
        'gr_id': review['book']['id']['#text'],
        'link': review['link'],
        'body': review['body'],
        'read_count': review['read_count'],
        'date_added': parse_date(review['date_added']),
        'date_updated': parse_date(review['date_updated']),
        'rating': review['rating']
    }


def has_review_a_body(review):
    return not has_review_no_body(review)


def has_review_no_body(review):
    return review['body'] is None


def date_to_ymd_format(dest_date):
    return dest_date.strftime('%Y-%m-%d')


def print_csv_header():
    print('#',
          'title',
          CSV_SEPARATOR,
          #   'isbn',
          #   CSV_SEPARATOR,
          'gr-id',
          CSV_SEPARATOR,
          'link',
          CSV_SEPARATOR,
          'body',
          CSV_SEPARATOR,
          'read-count',
          CSV_SEPARATOR,
          'date-added',
          CSV_SEPARATOR,
          'date-updated',
          CSV_SEPARATOR,
          'rating'
          )


def print_review_csv(review):
    print(
        review['title'],
        CSV_SEPARATOR,
        # review['isbn'],
        # CSV_SEPARATOR,
        review['gr_id'],
        CSV_SEPARATOR,
        review['link'],
        CSV_SEPARATOR,
        review['body'],
        CSV_SEPARATOR,
        review['read_count'],
        CSV_SEPARATOR,
        date_to_ymd_format(review['date_added']),
        CSV_SEPARATOR,
        date_to_ymd_format(review['date_updated']),
        CSV_SEPARATOR,
        review['rating']
    )


has_review = True
page = 1

reviews = []

while has_review:
    # https://www.goodreads.com/api/index#reviews.list
    resp = requests.get('https://www.goodreads.com/review/list/'+get_user_id()+'.xml',
                        params={'key': get_dev_key(), 'v': 2, 'id': get_user_id(), 'sort': 'review', 'page': page})

    data_dict = xmltodict.parse(resp.content)['GoodreadsResponse']
    book_reviews = [r for r in data_dict['reviews']['review']]

    book_reviews_filtered = list(filter(has_review_a_body, book_reviews))
    new_reviews = list(map(lambda x: reduce_review(x), book_reviews_filtered))

    reviews = reviews + new_reviews

    # until hit a book that has no review
    book_reviews_no_body = list(filter(has_review_no_body, book_reviews))
    if any(book_reviews_no_body):
        has_review = False
    else:
        page = page + 1
        # 1.1 second delay between requests, to meet quota
        time.sleep(1.1)


reviews = sorted(
    reviews, key=lambda r: r['date_updated'])

print(f"# Found {len(reviews)} book reviews")

print_csv_header()

list(map(lambda x: print_review_csv(x), reviews))
