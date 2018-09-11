# -*- coding: utf-8 -*-
__author__ = 'tomtiddler'

'''此文件仅用于测试，不用于生产过程'''

import requests

def get_auth_url():
    weibo_auth_url = "https://api.weibo.com/oauth2/authorize"
    redirect_url = "http://127.0.0.1/complete/weibo/"
    auth_url = weibo_auth_url+"?client_id={client_id}&redirect_uri={redirect_url}".\
        format(client_id=2473478422, redirect_url=redirect_url)

    print(auth_url)

def get_access_token(code):
    access_token_url = "https://api.weibo.com/oauth2/access_token"
    re_dict = requests.post(access_token_url, data={
        "client_id": 2473478422,
        "client_secret": "b1380a5ad6afcdfda02a35adc880ca20",
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": "http://127.0.0.1/complete/weibo/",
    })
    pass
    # b'{"access_token":"2.00NODyRDQj95hCab6215930dxxbwOE","remind_in":"157679999","expires_in":157679999,"uid":"3013908301","isRealName":"true"}'

def get_user_info(access_token="", uid=""):
    user_url = "https://api.weibo.com/2/users/show.json?access_token={access_token}&uid={uid}".format(access_token=access_token, uid=uid)

    print(user_url)

if __name__ == "__main__":
    # get_auth_url()
    # http://127.0.0.1/complete/weibo/?code=7bee2c5f37ab843efa3da97dc647ac59
    # get_access_token("aa61f05322c79bcfc45c4fcadbc129cf")
    get_user_info(access_token="2.00NODyRDQj95hCab6215930dxxbwOE", uid="3013908301")
