# 发生异常
try:
    a= 1/0
except Exception as e:
    print(e)
else:
    print("我是else")
finally:
    print("我是finally")

# 不发生异常
try:
    a= 1/1
except Exception as e:
    print(e)
else:
    print("我是else")
finally:
    print("我是finally")
