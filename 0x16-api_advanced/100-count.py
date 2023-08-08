#!/usr/bin/python3
"""
Another recursive fucntion
"""

import requests


def count_words(subreddit, word_list, word_count=None, after=None):
    """Recursively queries the Reddit API, parse the title of all hot articles,
    and prints a sorted count of given keywords.
    """
    if word_count is None:
        word_count = {}
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {'User-Agent': 'custom-user-agent'}
    params = {'after': after}
    response = requests.get(
        url,
        headers=headers,
        params=params,
        allow_redirects=False
    )

    if response.status_code == 200:
        data = response.json().get('data', {}).get('children', [])
        if data:
            for post in data:
                title = post.get('data', {}).get('title', '').lower()
                for word in word_list:
                    word = word.lower()
                    if title and title.count(word):
                        word_count[word] = word_count.get(
                                word, 0) + title.count(word)
            after = response.json().get('data', {}).get('after')
            if after:
                return count_words(subreddit, word_list, word_count, after)
            else:
                sorted_word_count = sorted(
                    word_count.items(),
                    key=lambda x: (-x[1], x[0])
                )
                for word, count in sorted_word_count:
                    print("{}: {}".format(word, count))
        else:
            return None
    else:
        return None


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
        print("Ex: {} programmin 'python java javascript'".format(sys.argv[0]))
    else:
        count_words(sys.argv[1], [x for x in sys.argv[2].split()])
