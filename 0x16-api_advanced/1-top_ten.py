#!/usr/bin/python3
"""
Returns first 10 hot posts
"""

import requests


def top_ten(subreddit):
    """Reddit API and prints the titles of the first 10 hot posts."""
    url = "https://www.reddit.com/r/{}/hot.json".format(subreddit)
    headers = {'User-Agent': 'custom-user-agent'}
    response = requests.get(url, headers=headers, allow_redirects=False)

    if response.status_code == 200:
        data = response.json().get('data', {}).get('children', [])
        if data:
            for post in data[:10]:
                print(post.get('data', {}).get('title'))
        else:
            print("No hot posts found for the subreddit.")
    else:
        print("None")


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print("Please pass an argument for the subreddit to search.")
    else:
        top_ten(sys.argv[1])
