"""
MQTT服务器 => 菜鸟驿站(统一中转站)
发布(PUB) => 快递员送包裹到驿站
订阅(SUB) => 用户从驿站取走自己的包裹
"""
# 需要有一个JSON数据
import json
# 看时间
import time
# 物流信息的盒子
# 如果说,这个包没有,报错了,那么我们需要将这个包给下载下来
# pip install paho-mqtt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
import paho.mqtt.client as mqtt
# 物流信息的盒子
received_message = []
# 将物流信息添加到消息盒子里面去
def on_message(client,userdata,msg):
    received_message.append(json.loads(msg.payload.decode()))
# 创建一个菜鸟驿站
client = mqtt.Client()
# 将菜鸟驿站的接通快递物流相关的信息
client.on_message = on_message
# 定义菜鸟驿站的地址
client.connect("127.0.0.1",21883,60)
# 菜鸟驿站的取件信息 -> 订阅
client.subscribe("bb")
# 菜鸟驿站的后台接听
client.loop_start()


# client.publish("aa",json.dumps({"conveyor":"run"}))
# print("已发送，启动传送带")
# time.sleep(2)
# client.publish("aa",json.dumps({"rod_control":"first_push"}))
# time.sleep(2)
# client.publish("aa",json.dumps({"rod_control":"first_pull"}))
# time.sleep(10)
def push_rod1(client):
    client.publish("aa", json.dumps({"rod_control": "first_push"}))

def pull_rod1(client):
    client.publish("aa", json.dumps({"rod_control": "first_pull"}))

# 1. 启动传送带
client.publish("aa", json.dumps({"conveyor": "run"}))
print("已发送，启动传送带")
time.sleep(2)

# 2. 连续推拉 10 次
for i in range(10):
    push_rod1(client)
    time.sleep(2)
    pull_rod1(client)
    time.sleep(2)