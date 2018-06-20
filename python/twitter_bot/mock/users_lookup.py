# coding: UTF-8

import json, config
from twitter_auth import get_auth

# 指定したユーザーの最新のツイートを取得？いやこれ多分ID検索

url = "https://api.twitter.com/1.1/users/lookup.json"  # なんだろうね

params = {'user_id': config.MC_ID, }

twitter = get_auth()
req = twitter.get(url, params=params)

if req.status_code == 200:

    timeline = json.loads(req.text)

    f = open('users_lookup.txt', 'w', encoding='utf-8')  # 書き込みモードで開く
    json.dump(timeline, f, ensure_ascii=False, indent=4)
    f.close()


else:
    print ("Error: %d" % req.status_code)