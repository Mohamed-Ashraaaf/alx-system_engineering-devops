#!/usr/bin/python3
"""
Recursive function querie Reddit API, parse title of all hot articles,
and prints a sorted count of given keywords.
"""
import requests


def count_words(subreddit, word_list, instances=None, after=None, count=0):
    if instances is None:
        instances = {}

    url = f"https://www.reddit.com/r/{subreddit}/hot/.json"
    headers = {
        "User-Agent": "linux:0x16.api.advanced:v1.0.0 (by /u/bdov_)"
    }
    params = {
        "after": after,
        "count": count,
        "limit": 100
    }

    response = requests.get(
            url, headers=headers, params=params, allow_redirects=False)

    try:
        results = response.json()
        if response.status_code == 404:
            raise Exception
    except Exception:
        print("")
        return

    results = results.get("data")
    after = results.get("after")
    count += results.get("dist")

    for c in results.get("children"):
        title = c.get("data").get("title").lower().split()
        for word in word_list:
            if word.lower() in title:
                times = len([t for t in title if t == word.lower()])
                if word in instances:
                    instances[word] += times
                else:
                    instances[word] = times

    if after is None:
        if not instances:
            print("")
            return
        sorted_instances = sorted(
                instances.items(), key=lambda kv: (-kv[1], kv[0]))
        for k, v in sorted_instances:
            print(f"{k}: {v}")
    else:
        count_words(subreddit, word_list, instances, after, count)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print(f"Usage: {sys.argv[0]} <subreddit> <list of keywords>")
        print(f"Ex: {sys.argv[0]} programing 'python java javascript'")
    else:
        count_words(sys.argv[1], sys.argv[2].split())
