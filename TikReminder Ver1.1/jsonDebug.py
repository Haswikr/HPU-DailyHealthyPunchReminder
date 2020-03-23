# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 21:09:04 2020

@author: Haswi
"""
#import json
#temp = json.loads({})
##temp.update({"new_key": "new_value"})
#temp[""]

wtblist = [{"class":"电气17-1","member":[{"name":"zhangsan","xh":"311705010200","dh":"15612345678"}]},{"class":"电气17-2","member":[{"name":"lisi","xh":"311808010100","dh":"18698765432"}]}]
wtblist = []
for i in range(2):
    if i == 0:
        bj = "电气17-3"
        xm = "张三"
        xh = "361708010111"
        dh = "18839123456"
    elif i == 1:
        bj = "电气17-3"
        xm = "李四"
        xh = "361708010111"
        dh = "18839123456"
        
    classIndex = -1
    for j in range(len(wtblist)):
        if bj == wtblist[j]["class"]:
            classIndex = j

    if not classIndex == -1:
        wtblist[classIndex]["member"].append({"name": xm, "xh": xh, "dh": dh})
    else:
        wtblist.append({"class":bj,"member":[{"name": xm, "xh": xh, "dh": dh}]})
    

#wtblist[0]["class"]
#          ["member"][0]["name"] ["xh"] ["dh"]
#                    [1]["name"] ["xh"] ["dh"]
#       [1]["class"]
#          ["member"][0]["name"] ["xh"] ["dh"]
#                    [1]["name"] ["xh"] ["dh"]