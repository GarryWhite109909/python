"""
通过YOLO实现成熟/半成熟/生的苹果分拣系统
"""
import base64       # 用于检测base64的图像字符串
import cv2          # OpenCV的图像处理
import numpy as np  # 数据转换
from ultralytics import YOLO # YOLO模型
import paho.mqtt.client as mqtt # MQTT客户端
import json         # 数据转换
import time         # 时间控制的包
import threading    # 多线程支持

# 定义一个变量,用户存储数据
received_messages = []

def on_message(client,userdata,msg):
    try:
        received_messages.append(json.loads(msg.payload.decode()))
    except Exception as e:
        print(f"消息解析错误: {e}")
# 初始化MQTT客户端
client = mqtt.Client()
client.on_message = on_message
client.connect("127.0.0.1",21883,60)
client.subscribe("bb")
client.loop_start()
    
