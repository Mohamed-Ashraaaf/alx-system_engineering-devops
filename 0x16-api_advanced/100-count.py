#!/usr/bin/python3
"""
Function to count words in all hot posts of a given Reddit subreddit.
"""
import requests


def count_words(subreddit, word_list, after=None, instances=None):
    if instances is None:
        instances = {word: 0 for word in word_list}

    if after is None:
        url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    else:
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?after={after}"

    headers = {
        "User-Agent": "linux:0x16.api.advanced:v1.0.0 (by /u/bdov_)"
    }

    response = requests.get(url, headers=headers, allow_redirects=False)

    if response.status_code == 404:
        print()
        return

    try:
        data = response.json().get("data")
        after = data.get("after")

        for post in data.get("children"):
            title = post.get("data").get("title").lower().split()
            for word in word_list:
                instances[word] += title.count(word.lower())

        if after is None:
            sorted_instances = sorted(
                    instances.items(), key=lambda x: (-x[1], x[0]))
            for word, count in sorted_instances:
                if count > 0:
                    print(f"{word}: {count}")
        else:
            count_words(subreddit, word_list, after, instances)

    except Exception:
        print()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <subreddit> <list of keywords>")
        print(f"Ex: {sys.argv[0]} programming 'python java javascript'")
    else:
        subreddit = sys.argv[1]
        word_list = sys.argv[2].split()
        count_words(subreddit, word_list)
