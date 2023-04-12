import requests
from auth_data import token
import json
import os


def get_wall_posts(group_name):
    url = f"https://api.vk.com/method/wall.get?domain={group_name}&count=40&access_token={token}&v=5.131"
    req = requests.get(url)
    src = req.json()


    # check if directory with group_name already exists
    if os.path.exists(group_name):
        print(f"directory with name {group_name} already exists")
    else:
        os.mkdir(group_name)

    with open(f"{group_name}/{group_name}.json", 'w', encoding='utf-8') as file:
        json.dump(src, file, indent=4, ensure_ascii=False)
    
    fresh_posts_id = []
    posts = src["response"]["items"]

    for fresh_post_id in posts:
        fresh_post_id = fresh_post_id["id"]
        fresh_posts_id.append(fresh_post_id)

    if not os.path.exists(f"{group_name}/exist_posts_{group_name}.txt"):
        print("No file with posts ID, creating new file!")
        with open(f"{group_name}/exist_posts_{group_name}.txt", "w") as file:
             for item in fresh_posts_id:
                 file.write(str(item) + "\n")

        for post in posts:

            post_id = post["id"]
            print(f"Sending post with id {post_id}")

            try:
                if "attachments" in post:
                    post = post["attachments"]
            except Exception:
                print(f"Something went wrong with post with {post_id}!")
    else: 
        print("Found file with posts ID, choosing the freshest IDs!")

def main():
    group_name = "spb1724" # "spb1724" #input("Введите название группы: ")
    get_wall_posts(group_name)

if __name__ == "__main__":
    main()