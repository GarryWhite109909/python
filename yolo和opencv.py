"""
如果我们想要opencv,那么我们需要导入一个包
    pip install opencv-python -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
    opencv 就是计算机视觉与机器学习的软件库
yolo => 模型
    pip install ultranlytics -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
    安防监控.....
"""
import cv2 # opencv的包,相当于给电脑安装眼睛
from ultralytics import YOLO # 导入YOLO模型,相当于给电脑安装大脑,识别图片当中物体
# 加载yolo模型
model = YOLO("yolo11n.pt")
# 打开摄像头
cap = cv2.VideoCapture(0)

# video_path = "./1.mp4"
# cap = cv2.VideoCapture(video_path)

# 循环播放视频里面的每一帧,相当于播放一步电影
while cap.isOpened():
    # 从视频当中读取每一帧的画面
    success,frame = cap.read()
    # 如果读取到的帧(画面)
    if success:
        # 用YOLO模型对当前的帧进行识别
        results = model(frame)
        # 在帧上面进行可视化推理,让YOLO识别,让它知道图片里面的哪里是人
        annotated_frame = results[0].plot()
        # 显示标注,相当于在图片里面找茬,所有的物品圈出来
        cv2.imshow("YOLOV8推理结果",annotated_frame)
        # 如果检查到键盘输出到了Q,那么就退出这个循环
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # 如果播放完毕,或者读取识别,那么直接退出循环
        break

# 释放视频捕获的对象,相当于关闭了播放器,释放资源
cap.release()
# 关闭所有的显示的窗口,相当于关机了
cv2.destroyAllWindows()