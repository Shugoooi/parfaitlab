# coding: UTF-8

import json, config
from twitter_auth import get_auth

# ユーザー検索（最初のツイートとかも取得される）

url = "https://api.twitter.com/1.1/users/search.json"  # ネームorIDで検索?

params = {'q': config.NS_SCREEN_NAME, }

twitter = get_auth()
req = twitter.get(url, params=params)

if req.status_code == 200:
    timeline = json.loads(req.text)

    f = open('out.txt', 'w', encoding='utf-8')
    json.dump(timeline, f, ensure_ascii=False, indent=4)
    f.close()


else:
    print("Error: %d" % req.status_code)
