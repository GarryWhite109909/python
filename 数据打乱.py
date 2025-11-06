import os       # 系统结构的包
import random   # 随机数的包

# 获取data目录当中文件列表
files = os.listdir("./data")
print(f"原文件顺序是:",files)

# 打乱文件列表的顺序
random.shuffle(files)
print(f"打乱文件顺序是:",files)