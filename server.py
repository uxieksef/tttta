from flask import Flask
import os
import requests
import json
import datetime
import time
from urllib import request

PORT = 8080
name = os.environ['NAME']
if name == None or len(name) == 0:
  name = "world"
MESSAGE = "auto compile again "
print("Message: '" + MESSAGE + "'")

app = Flask(__name__)


@app.route("/")
def root():
  print("starting...")
  loop_monitor_account()
  # loop_monitor_tracker()
  print("Handling web request. Returning message.started")
  result = MESSAGE.encode("utf-8")
  return result


def feishunotify_tr():

    # monitor webhook地址
    url = ""

    payload_message = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": "【项目】通知 - 告警",
                    "content": [
                        [
                            {
                                "tag": "at",
                                "user_id": "all"
                            },
                            {
                                "tag": "text",
                                "text": " 接口异常，\r\n【服务端】注意检查。 \r\n===================\r\n"
                            },
                            {
                                "tag": "a",
                                "text": "测试百度：",
                                "href": "https://www.baidu.com"
                            }
                        ]
                    ]
                }
            }
        }
    }
    headers = {

        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload_message))

    print(response.text)

def apichecker():
    url=''
    tt = requests.post(url=url)
    print(tt.text)
    jsonstr = json.loads(tt.text)
    if(jsonstr['message'] == 'success'):
        print('ssssss')
    else:
        feishunotify_tracker()
        print('failed')
        
def time_printer():
    now = datetime.datetime.now()
    ts = now.strftime('%Y-%m-%d %H:%M:%S')
    print('do func time :', ts)
def loop_monitor_tr():
    while True:
        time_printer()
        apichecker()
        time.sleep(3600)  # 暂停3600秒


        
#@app.route("/check")
#def rootcheck():
    #loop_monitor_tr()

  
##===================== 飞书通知账户信息 ==========================
def feishunotify_account(accountName, accountId, endDate, leftDay):

    # 账号监测 地址
    url = ""

    payload_message = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": "【账户】到期通知 - 告警 - "+ accountName,
                    "content": [
                        [
                            {
                                "tag": "at",
                                "user_id": "all"
                            },
                            {
                                "tag": "text",
                                "text": " \r\n【运营】注意检查。 \r\n【到期时间】"+endDate+"\r\n【剩余天数】"+leftDay+"\r\n===================\r\n"
                            },
                            {
                                "tag": "a",
                                "text": "测试百度地址",
                                "href": "https://www.baidu.com"
                            }
                        ]
                    ]
                }
            }
        }
    }
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=json.dumps(payload_message))

    print(response.text)
##===========账户检查========
def accountmonitor():

    data = request.urlopen("文件网络地址").read(100000)  # read only 100 000 chars
    print(data)
    data = data.decode().split("\r\n")  # then split it into lines

    for line in data:
        row = line.split("\t")
        print(row[2])
        interval = datetime.datetime.strptime(row[2], "%Y/%m/%d") - datetime.datetime.today()
        if(interval.days<30):
            print('目标日期与当前日期的日期差为：{}天'.format(interval.days))
            feishunotify_account(row[0], row[1], row[2], str(interval.days))
            print(line)
        else:
            print("==还早====")

def loop_monitor_account():
    while True:
        accountmonitor()
        time.sleep(86400)  # 暂停86400秒
  
@app.route("/mymonitor")
def mysqlcheck():
    #loop_monitor_account()
    return "started"



if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=PORT)
