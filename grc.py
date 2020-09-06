#! python3

import goodreads_api_client as gr


def read_file(filename):
    f = open(filename, "r")
    return f.read()


def get_dev_secret():
    return read_file("secret.credentials.txt")


def get_dev_key():
    return read_file("key.credentials.txt")


client = gr.Client(developer_key=get_dev_key(),
                   developer_secret=get_dev_secret())
book = client.Book.show('1128434')
keys_wanted = ['id', 'title', 'isbn']
reduced_book = {k: v for k, v in book.items() if k in keys_wanted}

print(reduced_book)
