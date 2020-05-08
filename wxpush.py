#-*- codeing = utf-8 -*-
#@Author: Angious
#@Time : 2020/5/8 9:54
#@File : wxpush.py
#@Software : PyCharm

import requests
import json
import yaml
import os


base_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?'
req_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='


class Push(object):
    def __init__(self):
        self.pushinfo = self._get_yaml()["wxinfo"]
        self.usrname = self.pushinfo["usrname"]
        self.agentid = self.pushinfo["agentid"]
        self.corpid = self.pushinfo["corpid"]
        self.corpsecret = self.pushinfo["corpsecret"]

    def get_access_token(self):
        urls = base_url + 'corpid=' + self.corpid + '8&corpsecret=' + self.corpsecret
        resp = requests.get(urls).json()
        access_token = resp['access_token']
        return access_token


    def get_message(self,msg):
        data = {
            "touser": self.usrname,
            "toparty": "@all",
            "totag": "@all",
            "msgtype": "text",
            "agentid": 1000002,
            "text": {
                "content": msg
            },
            "safe": 0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        data = json.dumps(data)
        return data

    def send_message(self,msg):
        data = self.get_message(msg)
        req_urls = req_url + self.get_access_token()
        res = requests.post(url=req_urls, data=data)
        print(res.text)

    def _get_yaml(self):
        """
        解析yaml
        :return: s  字典
        """
        path = os.path.join(os.path.dirname(__file__) + '/conf.yaml')
        f = open(path)
        s = yaml.load(f, Loader=yaml.FullLoader)
        f.close()
        if s is not None:
            return s
        else:
            print("conf content is None")



if __name__ == '__main__':
    s = Push()
    msg = '测试一下'
    s.send_message(msg)



