# 准备工作
import paho.mqtt.client as mqtt
import json
import os
import base64
import numpy as np
import cv2  # 导入Opencv,用于图像处理
import time

# 创建一个全局列表,用来存储接收到的数据(消息)
received_messages = []
# 定义个回调函数,当接收消息的时候执行
def on_message(client,userdata,msg):
    received_messages.append(msg.payload.decode())

# 创建一个MQTT的客户端
client = mqtt.Client()
# 设置接收消息的回调函数
client.on_message = on_message
# 连接到MQTT服务器
client.connect("127.0.0.1",21883,60)
# 订阅主题 bb
client.subscribe("bb")
# 启动后台接收消息
client.loop_start()

"""
从base64编码到OpenCV图像的完整转换流程
    1. 将base64编码字符串解码成二进制图片数据
    2. 将二进制的数据转换成numpy数组
    3. 将numpy数组解码成OpenCV可处理的图片对象数据
"""
def GetCvImage(jsonMsg,key):
    # 将base64编码字符串解码成二进制图片数据
    # jsonMsg 是一个字典,从字典当中 key_value,根据key获取value
    image_data = base64.b64decode(jsonMsg[key])
    # 将二进制的数据转换成numpy数组,每一个元素都是8位无符号的整数(0~255)
    image_array = np.frombuffer(image_data,np.uint8)
    # 将numpy数组解码成OpenCV可处理的图片对象数据
    image = cv2.imdecode(image_array,cv2.IMREAD_COLOR)
    # 返回处理好的图片
    return image

# 将设备传回来的图片,要存储到一个文件夹,叫做data
def make_dir(folder_path):
    # 检查folder_path是否存在
    if not os.path.exists(folder_path):
        # 没有存在
        print(f"{folder_path}不存在")
        os.makedirs(folder_path) # 创建目录文件
        print(f"{folder_path}已经创建好了")
    else:
        # 存在了
        print(f"{folder_path}已经存在,无需创建")

# 设置一个存储图片的目录路径
folder_path = "./data"
make_dir(folder_path)