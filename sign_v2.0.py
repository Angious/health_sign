#-*- codeing = utf-8 -*-
#@Author: Angious
#@Time : 2020/5/8 12:38
#@File : sign_v2.0.py
#@Software : PyCharm


from wxpush import Push
from work import SignIn
import schedule
import time

def run():
    s = SignIn()
    msg = s.work()
    Push().send_message(msg)

schedule.every().day.at("05:30").do(run) #设置每天05:30执行run函数
while True:
    schedule.run_pending()
    time.sleep(1)