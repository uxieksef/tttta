from flask import Flask
import os
import requests
import json
import datetime
import time

PORT = 8080
name = os.environ['NAME']
if name == None or len(name) == 0:
  name = "world"
MESSAGE = "auto compile again "
print("Message: '" + MESSAGE + "'")

app = Flask(__name__)


@app.route("/")
def root():
  print("Handling web request. Returning message.")
  result = MESSAGE.encode("utf-8")
  return result


def feishunotify():
    # 自定义关键词key_word
    key_word = "关键词"

    # 你复制的webhook地址
    url = "https://open.feishu.cn/open-apis/bot/v2/hook/966b4bd1-a0f3-417c-b2b9-2b17e4b48467"

    payload_message = {
        "msg_type": "post",
        "content": {
            "post": {
                "zh_cn": {
                    "title": "【项目】tracker通知 - 告警",
                    "content": [
                        [
                            {
                                "tag": "at",
                                "user_id": "all"
                            },
                            {
                                "tag": "text",
                                "text": " \r\n【项目】Tracker接口异常，\r\n【服务端】注意检查。 \r\n===================\r\n"
                            },
                            {
                                "tag": "a",
                                "text": "测试百度地址：",
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
    url='http://api.funnyplay.me/chkr/infer?cv=vtpcOsl5kXYxdJfE2do3tt7kGS9va42z81rkWal25IzhiaBCPGLRVJ406Ujv7vX2strM6cGmvssuilxutg0jCCKIpPTLwsYcf13/4XKc3Xx/EVCW1taPdCmQLXzVcKkRtx8FDS/ZtS4Scf0hUQSKbPpJXT5AjSWg1mTRMFbr5TCO3vXi0t5hlgdAKt7e532B'
    tt = requests.post(url=url)
    print(tt.text)
    jsonstr = json.loads(tt.text)
    if(jsonstr['message'] == 'success'):
        print('ssssss')
        feishunotify()
    else:
        print('failed')
        
def time_printer():
    now = datetime.datetime.now()
    ts = now.strftime('%Y-%m-%d %H:%M:%S')
    print('do func time :', ts)
def loop_monitor():
    while True:
        time_printer()
        apichecker()
        time.sleep(300)  # 暂停300秒

def dbtest():
    mydb = mysql.connector.connect(
    host="dbt3m-instance-1.c6oywpsw8kcj.us-east-1.rds.amazonaws.com",
     user="developer",
    password="1D2FDFBD7415232C",
    database="ym_novel"
  )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM ym_novel.novel_info where id=199")

    myresult = mycursor.fetchall()

    for x in myresult:
        print(x)
        
@app.route("/check")
def rootcheck():
 # apichecker()
  loop_monitor()

@app.route("/mymonitor")
def mysqlcheck():
    dbtest()



if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=PORT)
