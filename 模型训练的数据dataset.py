"""
模型训练的数据结构 => dataset
    dataset
        images
            train   => 用来训练的
            valid   => 用来验证的
            test    => 用来测试的
        labels
            train   => 用来训练的
            valid   => 用来验证的
            test    => 用来测试的
一般让
    训练数据集比例为85%,主要用于学习
    验证数据集比例为10%,用于调整优化
    测试数据集比例为5%,用于最终检验1
"""
import os
# 创建目录
os.makedirs('./dataset',exist_ok=True)
os.makedirs('./dataset/images',exist_ok=True)
os.makedirs('./dataset/images/train',exist_ok=True)
os.makedirs('./dataset/images/valid',exist_ok=True)
os.makedirs('./dataset/images/test',exist_ok=True)
os.makedirs('./dataset/labels',exist_ok=True)
os.makedirs('./dataset/labels/train',exist_ok=True)
os.makedirs('./dataset/labels/valid',exist_ok=True)
os.makedirs('./dataset/labels/test',exist_ok=True)
print("dataset目录结构创建完成")


# 先打乱数据
files = os.listdir('./data')
import random
random.shuffle(files)
print("打乱之后的数据",files)

# 将数据往dataset里面塞
import shutil # 导入文件操作的工具包,相当于请来一个文件搬运工
# 创建一个空列表来存储图片文件
images = []
# 遍历所有的文件,将文件丢到images盒子里面去
for file in files:
    # 文件名的最后三个字符
    if file[-3:] == 'jpg': # 检查文件的扩展名是否为jpg,只挑选图片文件
        images.append(file) # 将图片添加到images的盒子里去

# print(images)
# 获取图片的数量,看总共有多少张图片
images_count = len(images)
# print(images_count)

# 计算各数据集的图片数量,按比例分配
num_train = images_count * 0.85 # 训练数据集 85%
num_valid = images_count * 0.1  # 验证数据集 10%
num_test = images_count - num_train - num_valid # 剩下的就是测试数据集
print(f"训练数据集有:{num_train}个,验证数据集有:{num_valid},测试数据集有:{num_test}")






