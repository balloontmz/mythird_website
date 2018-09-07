# -*- coding: utf-8 -*-

"""推荐的第三方pip install pycryptodome"""

__author__ = 'tomtiddler'

import json
from datetime import datetime
from base64 import encodebytes, decodebytes, b64encode, b64decode
from urllib.parse import quote_plus, urlparse, parse_qs
from urllib.request import urlopen

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256


class Alipay(object):
    """
    支付宝支付接口
    """
    def __init__(self, appid, app_notify_url, app_private_key_path,
                 alipay_public_key_path, return_url, debug=False):
        self.appid = appid
        self.app_notify_url = app_notify_url
        self.return_url = return_url

        self.app_private_key_path = app_private_key_path
        self.app_private_key = None
        with open(self.app_private_key_path) as f:
            self.app_private_key = RSA.importKey(f.read())

        self.alipay_public_key_path = alipay_public_key_path
        with open(self.alipay_public_key_path) as f:
            self.alipay_public_key = RSA.importKey(f.read())

        if debug is True:
            self.__gateway = "https://openapi.alipaydev.com/gateway.do"
        else:
            self.__gateway = "https://openapi.alipay.com/gateway.do"

    def direct_pay(self, subject, out_trade_no, total_amount, return_url=None, **kwargs):
        biz_content = {
            "subject": subject,
            "out_trade_no": out_trade_no,
            "total_amount": total_amount,
            "product_code": "FAST_INSTANT_TRADE_PAY"
        }

        biz_content.update(kwargs)
        data = self.build_body("alipay.trade.page.pay", biz_content, return_url)
        return self.sign_data(data)

    def build_body(self, method, biz_content, return_url=None):
        data = {
            "app_id": self.appid,
            "method": method,
            "charset": "utf-8",
            "sign_type": "RSA2",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "1.0",
            "biz_content": biz_content
        }

        if return_url is not None:
            data["notify_url"] = self.app_notify_url
            data["return_url"] = self. return_url

        return data

    def sign_data(self, data):
        data.pop("sign", None)
        # 排序后的字符串
        unsign_items = self.ordered_data(data)
        unsign_string = "&".join("{0}={1}".format(k, v) for k, v in unsign_items)
        sign = self.sign(unsign_string.encode("utf-8"))
        quoted_string = "&".join("{0}={1}".format(k, quote_plus(v)) for k, v in unsign_items)

        # 获取最终的订单信息字符串
        signed_string = quoted_string + "&sign=" + quote_plus(sign)
        return signed_string

    def ordered_data(self, data):
        complex_keys = []
        for k, v in data.items():
            if isinstance(v, dict):
                complex_keys.append(k)

        # 将字典类型的数据dump出来 没懂
        for key in complex_keys:
            data[key] = json.dumps(data[key], separators=(",", ":"))

        return sorted([(k, v) for k, v in data.items()])

    def sign(self, unsigned_string):
        # 开始计算签名
        key = self.app_private_key
        signer = PKCS1_v1_5.new(key)
        signature = signer.sign(SHA256.new(unsigned_string))
        # base64编码， 转换为unicode表示并移除回车
        sign = encodebytes(signature).decode("utf8").replace("\n", "")
        return sign

    # def _verify(self, raw_content, signature):
    #     # 开始计算签名
    #     key = self.alipay_public_key
    #     signer = PKCS1_v1_5.new(key)
    #     digest = SHA256.new()
    #     digest.update(raw_content.encode("utf8"))
    #     if signer.verify(digest, decodebytes(signature.encode("utf8"))):
    #         return True
    #     return False
    #
    # def verify(self, data, signature):
    #     if "sign_type" in data:
    #         sign_type = data.pop("sign_type")
    #     # 排序后的字符串
    #     unsigned_items = self.ordered_data(data)
    #     message = "&".join(u"{}={}".format(k, v) for k, v in unsigned_items)
    #     return self._verify(message, signature)


if __name__ == "__main__":
    alipay = Alipay(
        appid="2016091600527206",
        app_notify_url="https://120.79.157.29",
        app_private_key_path="/home/tomtiddler/Documents/vue_shop/mythird_website/apps/trade/keys/app_private_key.pem",
        alipay_public_key_path="/home/tomtiddler/Documents/vue_shop/mythird_website/apps/trade/keys/alipay_public_key.pem",
        debug=True,
        return_url="https://120.79.157.29"
    )

    url = alipay.direct_pay(
        subject="测试订单",
        out_trade_no="2018090701",
        total_amount=100
    )
    re_url = "https://openapi.alipaydev.com/gateway.do?{data}".format(data=url)
    print(re_url)
    # 以下用于验证密钥正确性，没问题，需要再仔细检查参数
    # print(alipay.sign("a=123".encode("utf-8")))
