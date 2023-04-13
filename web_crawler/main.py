import time
from datetime import datetime
from time import sleep

import pandas as pd
import requests
from decouple import config

token = config("TOKEN")


def write_to_csv(data, path):
    df = pd.json_normalize(data)
    df.to_csv(path, index=False)


def get_data(post):
    try:
        post_id = post["id"]
    except:
        post_id = 0
    try:
        from_id = post["from_id"]
    except:
        from_id = 0
    try:
        likes = post["likes"]["count"]
    except:
        likes = "zero"
    try:
        reposts = post["reposts"]["count"]
    except:
        reposts = "zero"
    try:
        text = post["text"]
    except:
        text = "***"
    try:
        comments = post["comments"]["count"]
    except:
        comments = "zero"
    try:
        views = post["views"]["count"]
    except:
        views = "zero"
    try:
        date = post["date"]
    except:
        date = "zero"
    data = {
        "post_id": post_id,
        "from_id": from_id,
        "likes": likes,
        "reposts": reposts,
        "text": text,
        "comments": comments,
        "views": views,
        "date": date,
    }
    return data


def get_posts_by_q(q, start_time=1676025351):
    start = datetime.now()
    all_posts = []
    url = "https://api.vk.com/method/newsfeed.search"
    next_from = None
    params = {
        "q": q,
        "access_token": token,
        "v": 5.131,
        "count": 100,
        start_time: start_time,
    }
    while True:
        if next_from:
            params["start_from"] = next_from
        req = requests.get(url, params=params)
        src = req.json()
        if "error" in src:
            print(f'[ERROR] {src["error"]["error_msg"]}')
            break
        posts = src["response"]
        if "next_from" in posts:
            next_from = posts["next_from"]
        else:
            print("Something went wrong with next_from!")
            break

        for post in posts["items"]:
            data = get_data(post)
            all_posts.append(data)

        oldest_post_date = all_posts[-1]["date"]
        if oldest_post_date <= start_time:
            break
        sleep(0.4)

    write_to_csv(all_posts, "posts_SPbU.csv")

    print(len(all_posts))

    print(f"get_posts_by_q отработала за {str(datetime.now() - start)}")
    return all_posts


def main():
    q = "#СПбГУ"
    date_time = datetime(2023, 3, 13, 0, 0)
    start_time = int(time.mktime(date_time.timetuple()))
    get_posts_by_q(q, start_time=start_time)

if __name__ == "__main__":
    main()
