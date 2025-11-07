print("程序开始")
try:
    # 可能会出错的代码
    a = 10 / 0
except ZeroDivisionError:
    # 出错了,执行这里的代码
    print("除数不能为0")
else:
    # 没有出错,执行这里的代码
    print("程序没有出错")
finally:
    # 无论是否出错,都执行这里的代码
    print("程序结束")