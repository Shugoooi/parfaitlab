# from requests_oauthlib import OAuth1Session
import json
from twitter_auth import get_auth

url = "https://api.twitter.com/1.1/statuses/home_timeline.json"  # タイムライン取得用のURL

params = {'since': 2017-12-24, 'count': 100}

twitter = get_auth()
req = twitter.get(url, params = params)

if req.status_code == 200:

    timeline = json.loads(req.text)
    for tweet in timeline:
        print(tweet)

else:
    print("Error: %d" % req.status_code)
