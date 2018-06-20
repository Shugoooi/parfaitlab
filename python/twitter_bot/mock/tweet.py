# -*- coding:utf-8 -*-
from twitter_auth import get_auth

twitter = get_auth()
url = "https://api.twitter.com/1.1/statuses/update.json"

print("何をつぶやきますか?")
tweet = input('>> ')
print('----------------------------------------------------')

params = {"status": tweet}

req = twitter.post(url, params=params)

if req.status_code == 200:
    print("Succeed.")
else:
    print("ERROR : %d" % req.status_code)
