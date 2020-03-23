# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 12:30:14 2020

@author: Haswi
"""


import requests
import json
import CoolQ
import datetime
import time
import configparser

def getCookies():
    from selenium import webdriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    
    #driver = webdriver.Chrome("")
    
    driver.get("http://218.196.246.50/yqtj/mainpage ")

    element_keyword = driver.find_element_by_id('username')
    element_keyword.send_keys('账号')
    element_keyword = driver.find_element_by_id('password')
    element_keyword.send_keys('密码')
    
    botton = driver.find_element_by_id("login-submit")
    botton.click()
    cookie = driver.get_cookies() 
    Cookies = "JSESSIONID=" + cookie[0]["value"]
    #print(Cookies)   
    driver.quit()
    return(Cookies)


def readLocalCookies():
    f = open('cookies.ini', 'r')
    context = f.readlines()
    f.close()
    #print(context)
    return(context[0])
    
def saveLocalCookies(cookies):
    f = open('cookies.ini', 'w')
    f.write(cookies)
    f.close()

def getUnsignedList(Request_Cookies):
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
        'Cookie': Request_Cookies
                }
    data = {"page": 1,"rows": 500, "sort": "bj", "order": "asc"}
    response = requests.post("http://218.196.246.50/yqtj/xswbData", headers = headers, data = data)
    return(response.text)

def Doit(urgent = False):
    for i in range(5):
        cookies = readLocalCookies()
        if len(cookies) == 0:
            print("\n{}> cookies过期,尝试重新获取第{}次".format(i+1, n_time.strftime('%Y-%m-%d %H:%M:%S')))
            cookies = getCookies()
            saveLocalCookies(cookies)
        print("\n{}> 当前cookies：{}".format(cookies, n_time.strftime('%Y-%m-%d %H:%M:%S')))
        unsignedList = getUnsignedList(cookies)
        if unsignedList.count("统一身份认证"):
            print("\n{}> cookies过期,尝试重新获取第{}次".format(i+1, n_time.strftime('%Y-%m-%d %H:%M:%S')))
            cookies = getCookies()
            saveLocalCookies(cookies)
        else:
            break
        
    classContainer = [[],[],[],[],[],[],[],[],[],[],[],[]]
    #print(unsignedList)
    wtblist = json.loads(unsignedList)
    wtblist = wtblist["rows"]
    for i in range(len(wtblist)):
        bj = wtblist[i]["bj"]
        xm = wtblist[i]["xm"]
        xh = wtblist[i]["xh"]
        dh = wtblist[i]["lxdh"]
        if bj.count('电气合'):
            bjn = int(bj[-1])+7
        else:
            bjn = int(bj[-1])-1
            
        classContainer[bjn].append([bj,xm,xh,dh])
        
        #print(i,bj,xm,xh,dh)
    config = configparser.ConfigParser()
    config.read_file(open('config\config.ini', encoding="utf-8"))    
    if not int(config.get("状态","全部完成")):
        allClaFinished = CoolQ.sendUnsignedNotice(classContainer, urgent, int(config.get("群索引","班长群")))
        if allClaFinished:
            config.set("状态", "全部完成", "1")
            config.write(open('config\config.ini', "w", encoding="utf-8"))
    
    if not int(config.get("状态","合1完成")):
        myClaFinished = CoolQ.sendMyClassUnsignedNotice(8, classContainer, int(config.get("群索引","我的群")))
        if myClaFinished:
            config.set("状态", "合1完成", "1")
            config.write(open('config\config.ini', "w", encoding="utf-8"))
    #print(messageList)
    
#try:
config = configparser.ConfigParser()
config.read_file(open('config\config.ini', encoding="utf-8"))
startTime = config.get("时间设置", "开始时间")
urgeTime = config.get("时间设置", "催促时间")
intrevalTime = int(config.get("时间设置", "推送间隔"))
allFinished = int(config.get("状态","全部完成"))
if int(config.get("时间设置", "立即推送")):
    count = 60 * intrevalTime - 2
else:
    count = 0
while(True):
    s_time = datetime.datetime.strptime(str(datetime.datetime.now().date())+ startTime, '%Y-%m-%d%H:%M') 
    d_time = datetime.datetime.strptime(str(datetime.datetime.now().date())+ urgeTime, '%Y-%m-%d%H:%M') 
    r_time = datetime.datetime.strptime(str(datetime.datetime.now().date())+ '00:00', '%Y-%m-%d%H:%M') 
    n_time = datetime.datetime.now()

    if n_time > s_time:
        start = True
    else:
        start = False
    if n_time > d_time:
        urgent = True
    else:
        urgent = False
    count += 1  
    nextm, nexts = divmod(60 * intrevalTime - count, 60)
    if start:
        if not allFinished:
            print ("\r{}> 下次更新还有 {} min {} s  start:{} urgent:{}  ".format(n_time.strftime('%Y-%m-%d %H:%M:%S'), nextm, nexts, start, urgent), end="")
        else:
            print ("\r{}> 今日打卡已完成 同步配置:{} min {} s                   ".format(n_time.strftime('%Y-%m-%d %H:%M:%S'), nextm, nexts), end="")
    else:
        print ("\r{}> 同步配置:{} min {} s 启动时间:{}  start:{} urgent:{}  ".format(n_time.strftime('%Y-%m-%d %H:%M:%S'), nextm, nexts, s_time.strftime('%H:%M:%S'), start, urgent), end="")
    if count >= (60 * intrevalTime):
        config.read_file(open('config\config.ini', encoding="utf-8"))
        count = 0 
        if n_time > r_time and n_time < s_time and int(config.get("状态","全部完成")):
            config.set("状态", "全部完成", "0")
            config.set("状态", "合1完成", "0")
            config.write(open('config\config.ini', "w", encoding="utf-8"))
            print("\n{}> 重置完成状态".format(n_time.strftime('%Y-%m-%d %H:%M:%S')))
        allFinished = int(config.get("状态","全部完成"))
        if start and not allFinished:
            Doit(urgent)
    time.sleep(1)
    
#except Exception as r:
#    print(r)
