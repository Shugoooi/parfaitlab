# -*- coding:utf-8 -*-
import config
from requests_oauthlib import OAuth1Session

CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET


def get_auth():
    return OAuth1Session(CK, CS, AT, ATS)
