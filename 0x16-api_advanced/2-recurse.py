#!/usr/bin/python3
"""
Recursive function returning list
"""

import requests


def recurse(subreddit, hot_list=[], after=None):
    """Queries the Reddit API and returns a list of hot article titles."""
    url = 'https://www.reddit.com/r/{}/hot.json'.format(subreddit)
    headers = {'User-Agent': 'My User Agent'}
    params = {'limit': 100, 'after': after}
    response = requests.get(url, headers=headers, params=params, allow_redirects=False)

    if response.status_code == 200:
        data = response.json()['data']
        children = data['children']
        for child in children:
            hot_list.append(child['data']['title'])
        after = data['after']

        if after is None:
            return hot_list
        else:
            return recurse(subreddit, hot_list, after)
    else:
        return None

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        subreddit = sys.argv[1]
        result = recurse(subreddit)

        if result is not None:
            print(len(result))
        else:
            print("None")
