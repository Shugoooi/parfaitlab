# coding: UTF-8

import json, config
from twitter_auth import get_auth

# ユーザー検索（最初のツイートとかも取得される）

url = "https://api.twitter.com/1.1/users/show.json"  # ネームorIDで検索?

params = {'user_id': config.NS_ID, 'screen_name': config.NS_SCREEN_NAME, 'include_entities': False }

twitter = get_auth()
req = twitter.get(url, params=params)

if req.status_code == 200:
    timeline = json.loads(req.text)

    f = open('out.txt', 'w', encoding='utf-8')
    json.dump(timeline, f, ensure_ascii=False, indent=4)
    f.close()

else:
    print("Error: %d" % req.status_code)
