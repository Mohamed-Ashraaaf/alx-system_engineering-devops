#!/usr/bin/python3
"""
Count Words Module
"""
import requests
import sys


def count_words(subreddit, word_list, word_count=None, after=None):
    """Queries the Reddit API, parses titles, and prints keyword counts."""
    if word_count is None:
        word_count = {}

    base_url = 'https://www.reddit.com/r/{}/hot.json'.format(subreddit)
    headers = {'User-Agent': 'My User Agent'}
    params = {'after': after}

    response = requests.get(
            base_url, headers=headers, params=params, allow_redirects=False)

    if response.status_code == 200:
        data = response.json()['data']
        children = data['children']

        for child in children:
            title = child['data']['title'].lower()
            words = title.split()
            for word in word_list:
                if word.lower() in words:
                    if word in word_count:
                        word_count[word] += 1
                    else:
                        word_count[word] = 1

        if data['after'] is not None:
            return count_words(
                    subreddit, word_list, word_count, after=data['after'])
        else:
            sorted_words = sorted(
                    word_count.items(), key=lambda x: (-x[1], x[0]))
            for word, count in sorted_words:
                print("{}: {}".format(word, count))
    else:
        return


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
        print("Ex: {} programmin 'python java javascript'".format(sys.argv[0]))
    else:
        subreddit = sys.argv[1]
        word_list = sys.argv[2].split()
        count_words(subreddit, word_list)
