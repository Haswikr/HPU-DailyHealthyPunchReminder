# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 22:33:08 2020

@author: Haswi
"""

from urllib import parse
import requests
import json
import datetime
import configparser
import os
import random
host = "http://127.0.0.1:801/"


def sendUnsignedNotice(classContainer,showPhone):
    success, groupId = queryGroupId("班长群")
    if not success:
        return False
    classContainerLength = len(classContainer)
    finalText = "截至到{}未上报的名单：\n".format(nowTime(2))
    
    for i in range(classContainerLength):
        singleClassContainer = classContainer[i]["member"]
        className = classContainer[i]["class"]
        if showPhone:
            finalText += className + atClassMonitor(className) +"\n"
        else:
            finalText += className + "\n"
        for i in range(len(singleClassContainer)):
            name = singleClassContainer[i]["name"]
            stdId = singleClassContainer[i]["stdId"]
            phone = singleClassContainer[i]["phone"]
            
            if showPhone:
                finalText += name + " 电话：" + phone + "\n"
            else:
                finalText += stdId + " " + name + "\n"
       
        if len(finalText) > 2000:
            sendgroupMessage(groupId,finalText)
            print(finalText)
            finalText = ""
    finalText += "数据更新时间 {}".format(nowTime(2))
    if not classContainerLength:
        finalText = "今日打卡已全部完成  [CQ:at,qq=153720978]"
        finish = True
    else:
        finish = False    
    print(finalText)
    sendgroupMessage(groupId,finalText)
    #sendLeaderMessage(finalText)
    return(finish)
    
    
def sendMyClassUnsignedNotice(className, singleClassContainer):
    success, classId = queryGroupId(className)
    if success:
        finalText = "{}\n今日未完成健康上报的名单：\n".format(className)
        for i in range(len(singleClassContainer)):
            name = singleClassContainer[i]["name"]
            #stdId = singleClassContainer[i]["stdId"]
            #phone = singleClassContainer[i]["phone"]
            finalText += "{} {}\n".format(name,atMyClassStudent(className,name))  
        
        finalText += "数据更新时间 {} 耗时{:.2f}s\n请及时回复打卡情况！".format(nowTime(2), random.random())
        print(finalText)
        sendgroupMessage(classId,finalText)
    
    
def atClassMonitor(className):
    return(" [CQ:at,qq={}]".format(queryClassPersonId("班长群", className)))
    
def atMyClassStudent(className, stdname):
    return(" [CQ:at,qq={}]".format(queryClassPersonId(className, stdname)))


def sendgroupMessage(group, message):
    url = "send_msg?"
    para = parse.urlencode({'group_id':group,'message':message} )  
    response = requests.get(host + url + para) 
    retdata = json.loads(response.text)
    if retdata['retcode'] == 0:
        print("{}> 群 {} 消息发送成功 {}bit".format(nowTime(3), group, len(message)))
    else:
        print("{}> 群 {} 消息发送失败 Code:{}  {}bit".format(nowTime(3), group, retdata, len(message)))
        
def sendUserMessage(user, message):
    url = "send_msg?"
    para = parse.urlencode({'user_id':user,'message':message} )
    response = requests.get(host + url + para) 
    retdata = json.loads(response.text)
    if retdata['retcode'] == 0:
        print("{}> 好友 {} 消息发送成功 {}bit".format(nowTime(3), user, len(message))) 
    else:
        print("{}> 好友 {} 消息发送失败 Code:{}  {}bit".format(nowTime(3), user, retdata, len(message)))
    
def queryClassPersonId(classname, name):
    try:
        path = 'config\group\{}.ini'.format(classname)
        config = configparser.ConfigParser()
        config.read_file(open(path, encoding="utf-8"))
        value = config.get("成员", name)
        return(value)
    except:
        return("")
            
    
def queryGroupId(groupName):
    path = 'config\group\{}.ini'.format(groupName)
    if os.path.exists(path):
        try:
            config = configparser.ConfigParser()
            config.read_file(open(path, encoding="utf-8"))
            value = config.get("班级群", "群号")
            return True, value
        except:
            print(groupName,"查询群号失败")
            return False, None
    else:
        return False, None

def nowTime(length):
    time = datetime.datetime.now()
    if length == 1:
        time_r = time.strftime('%H')
    elif length == 2:
        time_r = time.strftime('%H:%M')
    else:
        time_r = time.strftime('%Y-%m-%d %H:%M:%S')
    return time_r
