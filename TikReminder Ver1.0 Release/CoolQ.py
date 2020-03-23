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

host = "http://127.0.0.1:801/"

def test():
    host = "http://127.0.0.1:801/"
    url = "send_msg?"
    #para = {'group_id':1059083065,'message':'你好 [CQ:at,qq=383661096]'}    
    para = {'user_id':383661096,'message':'你好 [CQ:at,qq=383661096]'}
      
    para = parse.urlencode(para) 
    response = requests.get(host + url + para) 
    print(json.loads(response.text))


def sendUnsignedNotice(classContainer,showPhone, groupId):

    finalText = "截至到{}未上报的名单：\n".format(nowTime(2))
    UnsignedNum = 0
    for i in range(12):
        cla = classContainer[i]
        if i <= 7:
            className = "电气17-{}".format(i+1)
        else:
            className = "电气合17-{}".format(i-7 )
        className += atClassMonitor(className)
        if len(cla):
            finalText += className + "\n"
            UnsignedNum += len(cla)
            #print("UnsignedNum", UnsignedNum)
        for j in range(len(cla)):
            if showPhone:
                finalText += cla[j][1] + " 电话：" + cla[j][3] + "\n"
            else:
                finalText += cla[j][2] + " " + cla[j][1] + "\n"
        if len(finalText) > 2000:
            sendgroupMessage(groupId,finalText)
            #print(finalText)
            finalText = ""
    if not UnsignedNum:
        finalText = "今日打卡已全部完成  [CQ:at,qq=153720978]"
        finish = True
    else:
        finish = False    
    #print(finalText)
    sendgroupMessage(groupId,finalText)
    #sendLeaderMessage(finalText)
    return(finish)
    
    
def sendMyClassUnsignedNotice(classId, classContainer, groupId):
    finalText = "截至到{}未上报的名单：\n".format(nowTime(2))
    cla = classContainer[classId]
    if len(cla):
        finish = False
        for j in range(len(cla)):
                finalText += "{} {} {}\n".format(cla[j][2],cla[j][1],atMyClassStudent(cla[j][1]))  
    else:
        finalText = "今日打卡已全部完成  [CQ:at,qq=383661096]"
        finish = True
    #print(finalText)
    sendgroupMessage(groupId,finalText)
    return(finish)
    
    
def atClassMonitor(name):
    return(" [CQ:at,qq={}]".format(querygroupPersonId("班长群", name)))
    
def atMyClassStudent(stdname):
    return(" [CQ:at,qq={}]".format(querygroupPersonId("电气合17-1", stdname)))

def sendLeaderMessage(message):
    #sendUserMessage(153720978, message)
    #sendUserMessage(383661096, message)
    pass

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

def queryPersonId(name):
    config = configparser.ConfigParser()
    config.read_file(open('config\friends.ini', encoding="utf-8"))
    
def querygroupPersonId(classname, name):
    config = configparser.ConfigParser()
    config.read_file(open('config\group.ini', encoding="utf-8"))
    value = config.get(classname, name)
    return(value)

def nowTime(length):
    time = datetime.datetime.now()
    if length == 1:
        time_r = time.strftime('%H')
    elif length == 2:
        time_r = time.strftime('%H:%M')
    else:
        time_r = time.strftime('%Y-%m-%d %H:%M:%S')
    return time_r