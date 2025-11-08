"""
通过YOLO实现成熟/半成熟/生的苹果分拣系统
"""
import base64  # 用于检测base64的图像字符串
import cv2  # OpenCV的图像处理
import numpy as np  # 数据转换
from ultralytics import YOLO  # YOLO模型
import paho.mqtt.client as mqtt  # MQTT客户端
import json  # 数据转换
import time  # 时间控制的包
import threading  # 多线程支持

# 定义一个变量,用户存储数据
received_messages = []


def on_message(client, userdata, msg):
    try:
        received_messages.append(json.loads(msg.payload.decode()))
    except Exception as e:
        print("消息解析错误")


# 初始化MQTT客户端
client = mqtt.Client()
client.on_message = on_message
client.connect("127.0.0.1", 21883, 60)
client.subscribe("bb")
client.loop_start()

# 启动传送带
client.publish("aa", json.dumps({"conveyor": "run"}))
print("传动带已经启动了")
time.sleep(2)


# 控制一号推杆的函数
def control_fruit():
    while True:
        # 让第一个杆子推出来
        client.publish("aa", json.dumps({"rod_control": "first_push"}))
        # 大概保持2秒的推杆状态
        time.sleep(2)
        # 拉回第一个杆子
        client.publish("aa", json.dumps({"rod_control": "first_pull"}))
        # 让杆子保持0.5秒状态
        time.sleep(0.5)


# control_fruit()
# 通过线程来启动一号推杆
# 相当于派一个工人专门负责一个推杆,不影响的主线程的工作
threading.Thread(target=control_fruit, daemon=True).start()

# 定义一个函数,用于定时打印队列状态
def print_queue_status():
    while True:
        print(f"[队列状态] 成熟水果: {len(firstSwitch_dat)}, 半成熟水果: {len(firstSwitch_dat2)}, 生水果: {len(firstSwitch_dat3)}")
        time.sleep(2)  # 每2秒打印一次

# 定义一个线程,用于定时打印队列状态
queue_status_thread = threading.Thread(target=print_queue_status)
queue_status_thread.daemon = True
queue_status_thread.start()

# 加载训练好的YOLO模型
model = YOLO("best.pt")
# 缓存分类三个队列，分别对应不同成熟度的水果
firstSwitch_dat = []      # 成熟水果队列
firstSwitch_dat2 = []     # 半成熟水果队列
firstSwitch_dat3 = []     # 生水果队列

# 定义统计变量
detection_stats = {
    'ripe': 0,      # 成熟水果检测次数
    'half_ripe': 0, # 半成熟水果检测次数
    'raw': 0,       # 生水果检测次数
    'total': 0,     # 总检测次数
    'low_confidence': 0  # 低置信度检测次数
}

# 代码比较多,也容易报错,所以我们使用try/except
try:
    # 主循环,持续的处理消息,相当于专注流水线的调度员
    while True:
        # 检索是否有新的消息到达
        if received_messages:
            # 取出里面的第一个消息
            json_msg = received_messages.pop(0)
            if "image" in json_msg:
                # 获取base64的编码的图像字符串
                imageDat = json_msg['image']
                # 解码成字节流
                image_data = base64.b64decode(imageDat)
                # 转换成numpy数组
                image_array = np.frombuffer(image_data, np.uint8)
                # 用OpenCV解码成彩色图像
                image = cv2.imdecode(image_array,cv2.IMREAD_COLOR)
                # 如果成功获取到了这个图片
                if image is not None:
                    # 使用YOLO模型进行推理
                    result = model.predict(image)[0] # 获取第一个图片的结果
                    # 获取所有边框检测的类别编号
                    cls_tensor = result.boxes.cls
                    # 如果只要检测到一个水果
                    if len(cls_tensor) > 0:
                        # 获取第一个检测结果的列表
                        cls = int(cls_tensor[0].item())
                        # 获取置信度
                        conf = float(result.boxes.conf[0].item())
                        print(f"检测类别: {cls}, 置信度: {conf:.4f}")
                        
                        # 更新总检测次数
                        detection_stats['total'] += 1
                        
                        # 设置置信度阈值，但不过于严格
                        if conf > 0.3:  # 降低置信度阈值，减少漏检
                            # 将列表编号加入到队列当中,等待传感器触发
                            firstSwitch_dat.append(cls)
                            print(f"检测结果已添加到队列，当前队列长度: {len(firstSwitch_dat)}")
                            
                            # 更新统计信息
                            if cls == 0:
                                detection_stats['ripe'] += 1
                            elif cls == 1:
                                detection_stats['half_ripe'] += 1
                            elif cls == 2:
                                detection_stats['raw'] += 1
                        else:
                            print(f"检测结果置信度过低，忽略：{conf:.4f}")
                            detection_stats['low_confidence'] += 1
                            
                        # 每10次检测打印一次统计信息
                        if detection_stats['total'] % 10 == 0:
                            print(f"[统计信息] 总检测: {detection_stats['total']}, 成熟: {detection_stats['ripe']}, 半成熟: {detection_stats['half_ripe']}, 生: {detection_stats['raw']}, 低置信度: {detection_stats['low_confidence']}")
                    else:
                        print("没有检测到任何的物品")
                else:
                    print("图像解码失败")

            # 收到第一个传感器的信号
            if 'first_switch' in json_msg:
                # 读取传感器的状态
                dat = json_msg['first_switch']
                print(f"成熟水果传感器状态: {dat}")
                # 当传感器被遮挡,一般就是False,表示有物体经过
                if not dat:
                    # 检测队列是否对对应的水果分类结果
                    if firstSwitch_dat:
                        # 取出最早的一个水果分类结果(与当前到达的水果匹配)
                        cls_val = firstSwitch_dat.pop(0)
                        print(f"处理水果，类别: {cls_val}, 队列剩余: {len(firstSwitch_dat)}")
                        # 如果说这个编号是0,成熟水果 - 推杆2
                        if cls_val == 0:
                            # 发送推出指令,控制第二个推杆（成熟苹果）
                            print("执行：推出成熟水果")
                            client.publish("aa", json.dumps({"rod_control":"second_push"}))
                            time.sleep(0.5)
                            client.publish("aa", json.dumps({"rod_control":"second_pull"}))
                        else:
                            # 非成熟水果,暂存第二个队列当中
                            firstSwitch_dat2.append(cls_val)
                            print(f"非成熟水果传递到下一队列: {cls_val}, 队列长度: {len(firstSwitch_dat2)}")
                    else:
                        # 传感器触发了,但是没有对应识别结果
                        print("警告,成熟水果传感器触发,但是没有对应的分类数据")

            # 收到第二个传感器的信号
            if 'second_switch' in json_msg:
                # 读取传感器的状态
                dat = json_msg['second_switch']
                print(f"半成熟水果传感器状态: {dat}")
                # 当传感器被遮挡,表示有物体经过
                if not dat:
                    # 检测第二个队列是否有分类结果
                    if firstSwitch_dat2:
                        # 取出最早的一个水果分类结果
                        cls_val = firstSwitch_dat2.pop(0)
                        print(f"处理水果，类别: {cls_val}, 队列剩余: {len(firstSwitch_dat2)}")
                        # 如果是半成熟苹果（class=1）- 推杆3
                        if cls_val == 1:
                            # 发送推出指令,控制第三个推杆（半成熟苹果）
                            print("执行：推出半成熟水果")
                            client.publish("aa", json.dumps({"rod_control":"third_push"}))
                            time.sleep(0.5)
                            client.publish("aa", json.dumps({"rod_control":"third_pull"}))
                        else:
                            # 生苹果,暂存第三个队列当中
                            firstSwitch_dat3.append(cls_val)
                            print(f"生水果传递到下一队列: {cls_val}, 队列长度: {len(firstSwitch_dat3)}")
                    else:
                        # 传感器触发了,但是没有对应识别结果
                        print("警告,半成熟水果传感器触发,但是没有对应的分类数据")

            # 收到第三个传感器的信号
            if 'third_switch' in json_msg:
                # 读取传感器的状态
                dat = json_msg['third_switch']
                print(f"生水果传感器状态: {dat}")
                # 当传感器被遮挡,表示有物体经过
                if not dat:
                    # 检测第三个队列是否有分类结果
                    if firstSwitch_dat3:
                        # 取出最早的一个水果分类结果
                        cls_val = firstSwitch_dat3.pop(0)
                        print(f"处理水果，类别: {cls_val}, 队列剩余: {len(firstSwitch_dat3)}")
                        # 如果是生苹果（class=2）- 推杆4
                        if cls_val == 2:
                            # 发送推出指令,控制第四个推杆（生苹果）
                            print("执行：推出生水果")
                            client.publish("aa", json.dumps({"rod_control":"fourth_push"}))
                            time.sleep(0.5)
                            client.publish("aa", json.dumps({"rod_control":"fourth_pull"}))
                        else:
                            # 未知类别，默认处理
                            print(f"未知类别苹果: {cls_val}")
                    else:
                        # 传感器触发了,但是没有对应识别结果
                        print("警告,生水果传感器触发,但是没有对应的分类数据")
        time.sleep(0.01)
# 一旦出现异常
except KeyboardInterrupt:
    print("程序被用户中断...")
# 无论有没有异常出现,他都执行
finally:
    # 发送停止传动带的指令
    client.publish("aa",json.dumps({"conveyor":"stop"}))
    print("发送停止传送带")

    # 释放MQTT资源
    client.loop_stop()
    client.disconnect()