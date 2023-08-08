#!/usr/bin/python3
"""
Returns the N# of subs for a given subreddit
"""

import requests


def number_of_subscribers(subreddit):
    """returns the number of subscribers for a given subreddit."""
    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)
    headers = {'User-Agent': 'custom-user-agent'}
    response = requests.get(url, headers=headers, allow_redirects=False)

    if response.status_code == 200:
        return response.json().get('data', {}).get('subscribers', 0)
    return 0


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        print("{:d}".format(number_of_subscribers(sys.argv[1])))
