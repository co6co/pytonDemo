#coding="utf-8"

import time
import functools 
'''
装饰器
'''
def foo()->None:
    '''
    定义方法(API)供外部使用
    '''
    print("执行 foo.。")

"""
有切面需求的场景，较为经典的有插入日志、性能测试、事务处理等。装饰器是解决这类问题的绝佳设计
"""
def timeFoo(func ):
    '''
    func: 需要包装的函数
    return: 包装好的函数
    '''
    print(type(func))
    def wrapper():
        start=time.time()
        result=func()
        end=time.time()
        print(f"{func.__name__} 用时：{end-start}")
        return result
    return wrapper

# 方法1
foo=timeFoo(func=foo)
foo()
print(f"手写装饰器：{foo.__name__}")

# 方法2 语法糖
@timeFoo    #foo = timeit(foo)完全等价
            #除了字符输入少了一些，还有一个额外的好处：这样看上去更有装饰器的感觉
def foo2():
    print("执行 foo2.。")

foo2()
print(f"使用语法糖：{foo2.__name__}")

# 方法3 内置装饰器
## staticmethod、classmethod和property，作用分别是把类中定义的实例方法变成静态方法、类方法和类属性
class Rabbit(object):
     
    def __init__(self, name):
        self._name = name
     
    @staticmethod
    def newRabbit(name):
        return Rabbit(name)
     
    @classmethod #将函数转换为类方法
    def classMethod(cls,firstName,secendName,*arg):
        return cls(firstName+secendName)
    
    def objectMethod(self):
        print("对象方法")
     
    @property
    def name(self):
        return self._name

'''
    @name.setter
    def name(self, name):
        self._name = name
'''   
rabbit=Rabbit.newRabbit("静态方法")
print(rabbit.name)

print (f"类方法:{type(rabbit.classMethod)},对象方法：{type(rabbit.objectMethod)}")
rabbit=rabbit.classMethod("类","方法") 
print(rabbit.name)

# 方法3 functools
def timeFoo2(func):
    '''
    assigned中的属性名将使用赋值的方式替换
    updated中的属性名将使用update的方式合并
    '''
    @functools.wraps(func)
    def wrapper():
        start=time.time()
        result=func()
        end=time.time()
        print(f"{func.__name__} 用时：{end-start}")
        return result
    return wrapper
@timeFoo2
def foo3():
    print("执行 foo3.。")

foo3() 
print(f"functools ：{foo3.__name__}")