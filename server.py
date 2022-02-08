from flask import Flask
import os
import requests
import json

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

        "msg_type": "text",
        "content": {

            "text": key_word + "测试信息如下"
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
        
        
@app.route("/check")
def rootcheck():
  apichecker()



if __name__ == "__main__":
  app.run(debug=True, host="0.0.0.0", port=PORT)
