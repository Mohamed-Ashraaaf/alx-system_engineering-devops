#!/usr/bin/python3
"""
Count Words Module
"""
import requests
import sys


def count_words(subreddit, word_list, after=None, counts=None):
    if after is None:
        after = ""
    if counts is None:
        counts = {}

    url = f"https://www.reddit.com/r/{subreddit}/hot.json?after={after}"
    headers = {"User-Agent": "reddit-api-script"}
    response = requests.get(url, headers=headers, allow_redirects=False)

    if response.status_code != 200:
        return

    data = response.json()["data"]
    children = data["children"]

    for post in children:
        title = post["data"]["title"].lower().split()
        for word in word_list:
            counts[word] = counts.get(word, 0) + title.count(word.lower())

    next_page = data["after"]
    if next_page is not None:
        count_words(subreddit, word_list, after=next_page, counts=counts)
    else:
        sorted_counts = sorted(
                counts.items(), key=lambda item: (-item[1], item[0]))
        for word, count in sorted_counts:
            print(f"{word}: {count}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <subreddit> <list of keywords>")
        print(f"Ex: {sys.argv[0]} programming 'python java javascript'")
    else:
        subreddit = sys.argv[1]
        word_list = sys.argv[2].split()
        count_words(subreddit, word_list)
