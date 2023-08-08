#!/usr/bin/python3
"""
Another recursive function
"""

import requests


def count_words(subreddit, word_list, after=None, count_dict={}):
    """
    Queries the Reddit API and counts the occurrences of keywords in titles.

    Args:
        subreddit (str): The name of the subreddit.
        word_list (list): A list of keywords to count.
        after (str, optional): The post ID to start querying from.
        count_dict (dict, optional): A dictionary to store keyword counts.

    Returns:
        None
    """
    if count_dict == {}:
        word_list = [word.lower() for word in word_list]

    headers = {
        'User-Agent': 'Mozilla/5.0 Windows NT 10.0; Win64; x64)'
        'AppleWebKit/537.36 (KHTML, like Gecko)'
        'Chrome/97.0.4692.71'
        'Safari/537.36'
    }
    params = {
        'sort': 'hot',
        'limit': 100,
        'after': after
    }

    url = 'https://www.reddit.com/r/{}/hot.json'.format(subreddit)
    response = requests.get(
            url, headers=headers, params=params, allow_redirects=False)

    if response.status_code == 200:
        data = response.json().get('data', {})
        children = data.get('children', [])

        for child in children:
            title = child['data']['title'].lower().split()

            for word in word_list:
                count_dict[word] = count_dict.get(word, 0) + title.count(word)

        after = data.get('after')
        if after:
            count_words(subreddit, word_list, after, count_dict)
        else:
            sorted_counts = sorted(
                    count_dict.items(), key=lambda item: (-item[1], item[0]))
            for word, count in sorted_counts:
                print('{}: {}'.format(word, count))
    else:
        return None


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
        print("Ex: {} programmin 'python java javascript'".format(sys.argv[0]))
    else:
        subreddit = sys.argv[1]
        word_list = sys.argv[2].split()
        count_words(subreddit, word_list)
