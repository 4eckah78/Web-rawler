import requests
import json
import os
from decouple import config

token = config('TOKEN')

def get_wall_posts(group_name, count):
    url = f"https://api.vk.com/method/wall.get?domain={group_name}&count={count}&access_token={token}&v=5.131"
    req = requests.get(url)
    src = req.json()
    return src["response"]["items"][0]["id"]
    

def main():
    group_name = "itmocup" # "spb1724" #input("Введите название группы: ")
    count = 1
    print(get_wall_posts("itmocup", 1)) # == 65!

if __name__ == "__main__":
    main()