from ultralytics import YOLO
model = YOLO("./runs/detect/train/weights/last.pt")
if __name__ == '__main__':
    results = model("./dataset/images/test/img110.jpg",imgsz=640)
    for result in results:
        if len(result.boxes) > 0:
            cls_index = int(result.boxes.cls[0])
            confidence = float(result.boxes.conf[0])
            class_name = result.names[cls_index]
            print(f"检测到类别: {class_name}, 置信度: {confidence:.4f}")
        else:
            print("未检测到任何目标")
        result.show()
