import os # 系统接口的一个包
# 定义一个目录文件
folder_path = "my_photos"
# 如果有这个文件夹,提示已经存在了,如果没有的话,我们就创建这个文件夹
if not os.path.exists(folder_path):
    print(f"{folder_path}不存在")
    # 创建这个目录
    os.makedirs(folder_path)
    print(f"{folder_path}已经创建成功了")
else:
    # 目录已经存在了,那么不需要创建了
    print(f"{folder_path}已经存在,无需创建")