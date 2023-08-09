
import datetime,sys,threading,os
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

 
LEVEL_LIST=["TRACE","DEBUG","INFO","SUCCESS","WARNING","ERROR","CRITICAL"]
folder="."
if os.name =="nt":folder="c:\log\python"
elif os.name =="posix":folder="./log"
 
for level in LEVEL_LIST:
    fileNamePart=f"{level}.log"
    p=os.path.join(folder,"loguru_{time:YY-MM}_"+fileNamePart)
    logger.add(p ,rotation="5 MB",level=level,encoding="utf-8" ,retention='7 days' ,format="{time:YY-MM-DD HH:mm:ss}\t{level}\t{file}\t{line}\t{message}")
 

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
def __log(msg,type:int=0,foregroundColor:int=37,bg=40,e=None,hasPrefix:bool=True):
    t=threading.currentThread()
    time = datetime.datetime.now() 
    err=e.__traceback__.tb_lineno if e !=None else ""
    prefix=f"['{time.strftime('%Y.%m.%d-%H:%M:%S')}'] [{t.ident}|{t.name}]\t"
    if not hasPrefix:prefix=""
    print(f"{prefix}\033[{type};{foregroundColor};{bg}m{msg}{err}\033[0m")
def log(msg):__log(msg)


def start_mark(msg,f="--",start:str="\r\n",end:str=">",num:int=36):
    __log(start+f*num+ msg +f*num+end,hasPrefix=False)
def end_mark(msg,f="==",start:str="\r\n<",end:str="\r\n\r\n",num:int=36):
    __log(start+f*num+ msg +f*num+end,hasPrefix=False)

def info(msg):__log(msg)

def succ(msg): __log(msg,7,32,40)

def warn(msg):__log(msg,7,33,40)

def err(msg,e=None):__log(msg,7,31,40,e)

def critical(msg):__log(msg,0,37,40)

if __name__ =="__main__":
    logger.trace("123456asdf")
    logger.success("*arg:{}{}\t\t**kwargs:'ab:{ab},cd:{cd}'","元数据1","元数据2",ab="字典数据1",cd="字典数据2")