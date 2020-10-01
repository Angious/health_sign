# -*- codeing = utf-8 -*-
# @Author: Angious
# @Time : 2020/5/8 9:54
# @File : job.py
# @Software : PyCharm

import requests
import json
import yaml
import os
from selenium import webdriver
import time
import random


def _get_yaml():
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


class Push(object):
    def __init__(self, usr, msg):
        self.base_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?'
        self.req_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='
        self.pushinfo = _get_yaml()["wxinfo"]
        self.usrname = self.pushinfo["usrname"]
        self.agentid = self.pushinfo["agentid"]
        self.corpid = self.pushinfo["corpid"]
        self.corpsecret = self.pushinfo["corpsecret"]
        self.usr = usr
        self.msg = msg

    def get_access_token(self):
        urls = self.base_url + 'corpid=' + self.corpid + '&corpsecret=' + self.corpsecret
        resp = requests.get(urls).json()
        access_token = resp['access_token']
        return access_token

    def send_message(self):
        data = self.get_message()
        req_urls = self.req_url + self.get_access_token()
        res = requests.post(url=req_urls, data=data)
        print(res.text)

    def get_message(self):
        data = {
            "touser": self.usr,
            "toparty": "@all",
            "totag": "@all",
            "msgtype": "text",
            "agentid": self.agentid,
            "text": {
                "content": self.msg
            },
            "safe": 0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        data = json.dumps(data)
        return data


def vpn_login():
    xh, sec = _get_yaml()["stuinfo"]["xh"], _get_yaml()["stuinfo"]["sec"]
    temp1 = random.randint(360, 369) * 0.1
    temp2 = random.randint(360, 369) * 0.1
    temp1 = str(temp1)[0:4]
    temp2 = str(temp2)[0:4]
    print("生成的随机体温为：", temp1, temp2)

    url = "https://ids.v.just.edu.cn:4443/cas/login?service=http%3A%2F%2Fmy.just.edu.cn%2F/"
    option = webdriver.ChromeOptions()
    # 无头模式
    # option.add_argument("headless")
    # option.add_argument("no-sandbox")
    # option.add_argument("disable-dev-shm-usage")

    browser = webdriver.Chrome(executable_path="chromedriver.exe", options=option)
    browser.get(url)
    time.sleep(2)

    browser.find_element_by_id("username").send_keys(xh)
    browser.find_element_by_id("password").send_keys(sec)
    browser.find_element_by_class_name("login_btn").click()
    time.sleep(2)

    browser.find_element_by_xpath("/html/body/div/div[2]/div[1]/div/div/div/div/div/div/ul/li[1]/div/div/div[2]").click()
    time.sleep(2)

    browser.find_element_by_xpath("xpath自己找一下吧，时间没到我进不去").send_keys(temp1)
    browser.find_element_by_xpath("xpath自己找一下吧，时间没到我进不去").send_keys(temp2)
    browser.find_element_by_id("id/class_name自己找一下吧，时间没到我进不去").click()
    time.sleep(2)

    browser.close()
    push = Push("ChenXXX", f"打卡成功，生成随机体温为{temp1},{temp2}")
    push.send_message()


if __name__ == '__main__':
    vpn_login()
