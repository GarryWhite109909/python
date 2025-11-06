import paho.mqtt.client as mqtt
import json
import os
import base64
import numpy as np
import cv2  
import time
received_messages = []
def on_message(client,userdata,msg):
    received_messages.append(json.loads(msg.payload.decode()))
client = mqtt.Client()
client.on_message = on_message
client.connect("127.0.0.1",21883,60)
client.subscribe("bb")
client.loop_start()
def GetCvImage(jsonMsg,key):
    image_data = base64.b64decode(jsonMsg[key])
    image_array = np.frombuffer(image_data,np.uint8)
    image = cv2.imdecode(image_array,cv2.IMREAD_COLOR)
    return image
def make_dir(folder_path):
    if not os.path.exists(folder_path):
        print(f"{folder_path}不存在")
        os.makedirs(folder_path)
        print(f"{folder_path}已经创建好了")
    else:
        print(f"{folder_path}已经存在,无需创建")
folder_path = "./data"
make_dir(folder_path)
i = 1
print("开始监听图片消息")
while True:
    if received_messages:
        msg_data = received_messages.pop(0)
        if 'image' in msg_data:
            print(f"接收到的是图像:{msg_data}")
            image = GetCvImage(msg_data,'image')
            cv2.imwrite(folder_path + "/" + f"img{i}.jpg",image)
            print(f"图片{i}已经保存了")
            i += 1
    time.sleep(0.01)