import math
from ultralytics import YOLO
model = YOLO("yolo11n.pt")
if __name__ == '__main__':
    model.train(data="./dataset/mydata.yaml", epochs=50)
    metrics = model.val()
    print("======模型的评估结果======")
    print(f"精度(mAP50): {metrics.box.map50:.4f}")
    print(f"平均精度(mAP50-95): {metrics.box.map:.4f}")
    print(f"精确率: {metrics.box.mp:.4f}")
    print(f"召回率: {metrics.box.mr:.4f}")
    results = model("./dataset/images/test/img148.jpg")
    for result in results:
        result.show()