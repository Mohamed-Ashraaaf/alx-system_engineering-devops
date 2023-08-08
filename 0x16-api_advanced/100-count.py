#!/usr/bin/python3
"""
100-count
"""

import requests


def count_words(subreddit, word_list, after=None, word_count={}):
    """Recursively queries the Reddit API, parse the title of all hot articles,
    and prints a sorted count of given keywords.
    """
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
                        if word in word_count:
                            word_count[word] += title.count(word)
                        else:
                            word_count[word] = title.count(word)
            after = response.json().get('data', {}).get('after')
            if after:
                return count_words(subreddit, word_list, after, word_count)
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
