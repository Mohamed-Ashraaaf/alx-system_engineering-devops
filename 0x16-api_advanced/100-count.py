#!/usr/bin/python3
"""
Function to count words in all hot posts of a given Reddit subreddit.
"""
import requests
import sys


def count_words(subreddit, word_list, after=None, instances=None):
    """
    Prints counts of given words found in hot posts of a given subreddit.

    Args:
        subreddit (str): The subreddit to search.
        word_list (list): The list of words to search for in post titles.
        after (str): The parameter for the next page of the API results.
        instances (dict): Key/value pairs of words/counts.
    """
    if instances is None:
        instances = {word.lower(): 0 for word in word_list}

    url = f"https://www.reddit.com/r/{subreddit}/hot/.json"
    headers = {"User-Agent": "linux:0x16.api.advanced:v1.0.0 (by /u/bdov_)"}
    params = {"after": after, "limit": 100}
    response = requests.get(
            url, headers=headers, params=params, allow_redirects=False)

    try:
        results = response.json()["data"]
        if response.status_code == 404:
            raise Exception
    except Exception:
        print("")
        return

    after = results.get("after")
    children = results.get("children")

    for c in children:
        title = c.get("data").get("title").lower().split()
        for word in word_list:
            if word.lower() in title:
                instances[word.lower()] += title.count(word.lower())

    if after is None:
        sorted_instances = sorted(
            instances.items(), key=lambda kv: (-kv[1], kv[0])
        )
        for word, count in sorted_instances:
            if count > 0:
                print(f"{word}: {count}")
    else:
        count_words(subreddit, word_list, after, instances)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
        print("Ex: {} programmin 'python java javascript'".format(sys.argv[0]))
    else:
        subreddit = sys.argv[1]
        word_list = sys.argv[2].split()
        count_words(subreddit, word_list)
