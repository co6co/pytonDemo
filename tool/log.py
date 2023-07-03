
import datetime,sys,threading
from loguru import logger

logger.remove()
logger.add(sys.stdout,level="INFO",format="{file}\t{line}\t{message}")
'''
#https://blog.csdn.net/Kangyucheng/article/details/112794185
TRACE           5   trace()
DEBUG           10  debug()
INFO            20  info()
SUCCESS         25  success()
WARNING         30  warning()
ERROR           40  error()
CRITICAL        50  critical()
'''

logger.add("c:\log\python\loguru_{time:YY-MM-DD_HH}_INFO.log",rotation="5 MB",level="INFO",encoding="utf-8" ,retention='7 days' ,format="{level}\t|{time:YY-MM-DD HH:mm:ss}\t|{file}\t|{line}\t|\t{message}")
logger.add("c:\log\python\loguru_{time:YY-MM-DD_HH}_ERROR.log",rotation="5 MB",level="ERROR",encoding="utf-8" ,retention='7 days' ,format="{level}\t|{time:YY-MM-DD HH:mm:ss}\t|{file}\t|{line}\t|\t{message}")

'''
\033[显示方式;前景色；背景色m*******\033[0m
\033[显示方式;前景色；背景色m*******\033[0m
显示方式:    0:默认值
            1:高亮
            4:下划线
            5:闪烁
            7:反显
            8:不可见
控制台颜色值：
前景色      背景色      颜色说明
 30           40        黑色
 31           41        红色
 32           42        绿色
 33           43        黄色
 34           44        蓝色
 35           45        紫红色
 36           46        青蓝色
 37           47        白色
'''
def __log(msg,type:int=0,foregroundColor:int=37,bg=40):
    t=threading.currentThread()
    time = datetime.datetime.now()
    print(f"['{time.strftime('%Y.%m.%d-%H:%M:%S')}'] [{t.ident}|{t.name}]\t\033[{type};{foregroundColor};{bg}m{msg}\033[0m")
def log(msg):
    __log(msg)

def succ(msg):
    __log(msg,7,32,40)

def warn(msg):
    __log(msg,7,33,40)

def err(msg):
    __log(msg,7,31,40)