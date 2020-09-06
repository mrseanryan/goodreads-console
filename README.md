# goodreads-console README

A simple console for retrieving data from Goodreads.

## Usage

```
grc-show-reviews.py
```

Your reviews are dumped out, in CSV format:

```
# Found 27 book reviews
# title _ gr-id _ link _ body _ read-count _ date-added _ date-updated _ rating
Heroes: Mortals and Monsters, Quests and Adventures (Stephen Fry's Great Mythology, #2) _ 41433634 _ https://www.goodreads.com/review/show/3033048494 _ Readable and cohesive - yet the whimsical humour is at times a little irritating. Seems to lack the gravitas of a conventional translation.<br /><br />Good footnotes, but no image attributions (who painted those lovely paintings?) _ 1 _ 2019-11-01 _ 2019-11-14 _ 3
...
```

A '\_' seperator is used, in order avoid the review text getting split up when imported into _Google Sheets_ or other tool.

## Setup

1. Get Goodreads API key

https://www.goodreads.com/api/keys

2. Save the key to this file:

```
key.credentials.txt
```

2. Save the secret to this file:

```
secret.credentials.txt
```

3. Save your user id to this file:

```
user-id.credentials.txt
```

tip: to get your user id, go to https://www.goodreads.com/ then click on **My Books**. You will see the user id in the URL.

3. Install Python 3.7.x and pip

- Python 3.7.9 or later
- pip 20.2.2 or later

4. Install dependencies

```
pip3 install -r pip.config
```

## References

### Goodreads API

https://www.goodreads.com/api/index

### Python library

https://github.com/mdzhang/goodreads-api-client-python

## License

License is [MIT](./LICENSE)
