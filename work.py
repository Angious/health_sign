#-*- codeing = utf-8 -*-
#@Author: Angious
#@Time : 2020/5/8 11:15
#@File : work.py
#@Software : PyCharm


from selenium import webdriver
import time
import random
import os
import yaml

class SignIn():
    def __init__(self):
        self.stuinfo = self._get_yaml()["stuinfo"]
        self.xh = self.stuinfo["xh"]
        self.vpn_sec = self.stuinfo["vpn_sec"]
        self.sec = self.stuinfo["sec"]
        # -----服务器端请取消这段注释，这段代码的意思是设置浏览器模式为无头模式（无界面模式）----#
        self.option = webdriver.ChromeOptions()
        # self.option.add_argument('headless')
        # self.option.add_argument('no-sandbox')
        # self.option.add_argument('disable-dev-shm-usage')
        self.option.add_argument('--ignore-certificate-errors')

        # webdriver路径配置
        # linux
        # driver = webdriver.Chrome('/usr/bin/chromedriver',chrome_options=option)
        # Pycharm
        self.driver = webdriver.Chrome(executable_path="D:\Code\Python_settings/chromedriver.exe", options=self.option)

    def signin(self):

        url = 'https://vpn.just.edu.cn/'
        self.driver.get(url)
        self.driver.find_element_by_id('username').send_keys(self.xh)
        self.driver.find_element_by_id('password').send_keys(self.vpn_sec)
        self.driver.find_element_by_id('btnSubmit_6').click()
        time.sleep(1)
        try:
            self.driver.find_element_by_id('btnContinue').click()
        except:
            pass

        self.driver.get('https://vpn.just.edu.cn/cas/,DanaInfo=ids2.just.edu.cn+login?service=http://my.just.edu.cn/')
        time.sleep(1)
        self.driver.find_element_by_id('username').send_keys(self.xh)
        self.driver.find_element_by_id('password').send_keys(self.sec)
        self.driver.find_element_by_class_name('login_btn').click()
        time.sleep(1)
        self.driver.get('https://vpn.just.edu.cn/default/work/jkd/jkxxtb/,DanaInfo=ehall.just.edu.cn+jkxxcj.jsp')
        self.driver.quit()


    def work(self):
        #登录
        self.signin()
        temp1 = random.randint(360, 369) * 0.1
        temp2 = random.randint(360, 369) * 0.1
        temp1 = str(temp1)[0:4]
        temp2 = str(temp2)[0:4]
        print("生成的随机体温为：",temp1,temp2)
        msg = "生成的随机体温为："+temp1+'，'+temp2+'\n'
        time.sleep(2)
        try:
            self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[1]/div/div/form/div[3]/div[16]/div[2]/div/div[2]/div/div/input').send_keys(temp1)
            self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[1]/div/div/form/div[3]/div[17]/div/div/div[2]/div/div/input').send_keys(temp2)
            time.sleep(1)
            if self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/div/div/button[1]'):
                try:
                    self.driver.find_element_by_xpath('/html/body/div[2]/div/div/div/div[2]/div/div/button[1]').click()
                    msg += '提交成功'
                except:
                    print('提交失败')
                    msg += '提交失败'
            else:
                print('未找到提交按钮')
                msg += '未找到提交按钮'
        except:
            msg +='警告：打卡失败，请手动检查'
        self.driver.quit()
        return msg


    # def test(self):
    #     import requests
    #     url = 'http://my.just.edu.cn/_web/fusionportal/ykt.jsp?'
    #     headers = {
    #         "Accept": "text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01",
    #         "Accept-Encoding": "gzip, deflate",
    #         "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    #         "Connection": "keep-alive",
    #         "Cookie": "HttpOnly; route=a047fc801448915ba46aeaaf2e20a3ac; JSESSIONID=C7F588EA9C648E083066E7955E69C3E5; sudyLoginToken=expired; HttpOnly; iPlanetDirectoryPro=AQIC5wM2LY4SfczSFFDlGYE1DDrR9%2BssE4yJrAHJGFsgfXo%3D%40AAJTSQACMDE%3D%23; language=",
    #         "Host": "my.just.edu.cn",
    #         "Referer": "http://my.just.edu.cn/_s2/students_sy/main.psp",
    #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36",
    #         "X-Requested-With": "XMLHttpRequest"
    #     }
    #     params = {
    #         "_p": "YXM9MiZ0PTImZD0xMDEmcD0xJmY9MzAmbT1OJg__",
    #         "timeStamp": "1586473542514",
    #         "callback": "jQuery22306817913968799607_1586473541943",
    #         "_": "1586473541944"
    #     }
    #     resp = requests.get(url, headers=headers, params=params)
    #     yue = resp.text
    #     data = yue[75:-104]
    #     print(data)
    #     return data
    #     # print("您的余额是：",data,"元")


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


