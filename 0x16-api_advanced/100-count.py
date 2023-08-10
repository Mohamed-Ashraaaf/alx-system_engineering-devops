#!/usr/bin/python3
"""
Recursive function to count words in hot articles of a Reddit subreddit.
"""
import requests


def count_words(subreddit, word_list, word_count=None, after=None):
    if word_count is None:
        word_count = {}

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "linux:0x16.api.advanced:v1.0.0 (by /u/bdov_)"}
    params = {"limit": 100}
    if after:
        params["after"] = after

    response = requests.get(
            url, headers=headers, params=params, allow_redirects=False)

    if response.status_code == 200:
        data = response.json()["data"]
        posts = data["children"]

        for post in posts:
            title = post["data"]["title"].lower()
            for word in word_list:
                word_count[word] = word_count.get(
                        word, 0) + title.count(word.lower())

        after = data.get("after")
        if after:
            return count_words(subreddit, word_list, word_count, after)

    sorted_count = sorted(
            word_count.items(), key=lambda item: (-item[1], item[0]))
    for word, count in sorted_count:
        print(f"{word}: {count}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
        print("Ex: {} programming 'python java javascript'".format(
            sys.argv[0]))
    else:
        subreddit = sys.argv[1]
        word_list = sys.argv[2].split()
        count_words(subreddit, word_list)
