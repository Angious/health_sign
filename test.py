
from selenium import webdriver
import time
import random


def vpn_login(xh, sec):
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


if __name__ == '__main__':
    vpn_login('18221060xxxx', 'xxxxxx')