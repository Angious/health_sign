#-*- codeing = utf-8 -*-
#@Author: Angious
#@Time : 2020/5/3 9:20
#@File : sign_v1.0.py
#@Software : PyCharm

#-------------V1.0------------

from selenium import webdriver
import time
import random
import requests
import schedule

option = webdriver.ChromeOptions()
option.add_argument('--ignore-certificate-errors') #忽略警告（连接VPN时会弹出...不是私密链接云云，加上这句表示忽略警告，继续访问）
#-----服务器端请取消这段注释，这段代码的意思是设置浏览器模式为无头模式（无界面模式）----#
# option.add_argument('headless')
# option.add_argument('no-sandbox')
# option.add_argument('disable-dev-shm-usage')

#-----------配置信息------------#
#个人信息配置
xh = '182210600000' #学号
vpn_sec = 'xxxxxx'  #VPN密码  一般是身份证后六位
sec = 'xxxxxx'      #信息门户密码   一般是身份证后六位
wxpush_usr = 'XXX'
#webdriver路径配置，chromedriver路径写你自己的
#webdriver配置参考readme文档
#linux
#driver = webdriver.Chrome('/usr/bin/chromedriver',chrome_options=option)
#Pycharm
driver = webdriver.Chrome(executable_path="D:\Code\Python_settings/chromedriver.exe",chrome_options=option)
#wxpusher微信消息推送服务，你需要前往wxpusher.zjiecode.com/admin/注册应用，使用说明参考官方文档wxpusher.zjiecode.com/
APPToken='AT_xxxxxxxxxxxx'   #你创建应用的APPToken
UID='UID_xxxxxxxxxx'         #你在微信查看自己的UID

def wxpush(msg):
    try:
        url = 'http://wxpusher.zjiecode.com/api/send/message/?appToken='+APPToken+'&content='+ msg + '&uid='+UID
        res = requests.get(url)
        print(res.text)
        print("微信推送成功，发送内容：")
        print(msg)
    except Exception as result:
        print("微信推送失败，请检查配置信息！")
        print(result)

def signin():
    url = 'https://vpn.just.edu.cn/'
    driver.get(url)
    driver.find_element_by_id('username').send_keys(xh)
    driver.find_element_by_id('password').send_keys(vpn_sec)
    driver.find_element_by_id('btnSubmit_6').click()
    time.sleep(1)
    try:
        driver.find_element_by_id('btnContinue').click()
    except:
        pass

    driver.get('https://vpn.just.edu.cn/cas/,DanaInfo=ids2.just.edu.cn+login?service=http://my.just.edu.cn/')
    time.sleep(1)
    driver.find_element_by_id('username').send_keys(xh)
    driver.find_element_by_id('password').send_keys(sec)
    driver.find_element_by_class_name('login_btn').click()
    time.sleep(1)
    driver.get('https://vpn.just.edu.cn/default/work/jkd/jkxxtb/,DanaInfo=ehall.just.edu.cn+jkxxcj.jsp')

def work():
    #登录
    signin()
    #随机生成两个36.0-36.9的体温，转换为长度为4的字符串
    temp1 = random.randint(360, 369) * 0.1
    temp2 = random.randint(360, 369) * 0.1
    temp1 = str(temp1)[0:4]
    temp2 = str(temp2)[0:4]
    print("生成的随机体温为：",temp1,temp2)
    msg = "生成的随机体温为："+temp1+'，'+temp2+'\n'

    #---------页面变更后这段可能需要修改--------
    driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[1]/div/div/form/div[3]/div[16]/div[2]/div/div[2]/div/div/input').send_keys(temp1)
    driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[1]/div/div/form/div[3]/div[17]/div/div/div[2]/div/div/input').send_keys(temp2)
    #----------------------------------------
    time.sleep(1)
    if driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/div/div/button[1]'):
        try:
            driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/div/div/button[1]').click()
            msg += '提交成功'
        except:
            print('提交失败')
            msg += '提交失败'
    else:
        print('未找到提交按钮')
        msg += '未找到提交按钮'
    driver.quit()
    return msg

def run():
    wxpush(work())

#wxpush('微信推送服务测试成功')#测试微信推送服务

#run()

schedule.every().day.at("07:30").do(run) #设置每天07:30执行run函数
while True:
    schedule.run_pending()
    time.sleep(1)
