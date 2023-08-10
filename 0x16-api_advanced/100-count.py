#!/usr/bin/python3
"""
Count Words Module
"""
import requests
import sys


def count_words(subreddit, word_list, after=None, word_count=None):
    if after is None:
        after = ""
    if word_count is None:
        word_count = {}

    url =
    "https://www.reddit.com/r/{}/hot.json?after={}".format(subreddit, after)
    headers =
    {"User-Agent": "python:com.example.myredditapp:v1.0.0 (by /u/username)"}
    response = requests.get(url, headers=headers, allow_redirects=False)

    if response.status_code != 200:
        return

    data = response.json()["data"]
    children = data["children"]

    for post in children:
        title = post["data"]["title"].lower()
        words = title.split()
        for word in word_list:
            if word.lower() in words:
                if word in word_count:
                    word_count[word] += 1
                else:
                    word_count[word] = 1

    next_page = data["after"]
    if next_page is not None:
        count_words(
                subreddit, word_list, after=next_page, word_count=word_count)
    else:
        sorted_words = sorted(
                word_count.items(), key=lambda x: (-x[1], x[0]))
        for word, count in sorted_words:
            print("{}: {}".format(word, count))


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
        print("Ex: {} programmin 'python java javascript'".format(sys.argv[0]))
    else:
        subreddit = sys.argv[1]
        word_list = sys.argv[2].split()
        count_words(subreddit, word_list)
