
import datetime,sys
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

logger.add("c:\log\python\loguru_{time:YY-MM-DD_HH}_INFO.log",level="INFO",encoding="utf-8" ,rotation="00:00" ,retention='7 days' ,format="{level}\t|{time:YY-MM-DD HH:mm:ss}\t|{file}\t|{line}\t|\t{message}")
logger.add("c:\log\python\loguru_{time:YY-MM-DD_HH}_ERROR.log",level="ERROR",encoding="utf-8" ,rotation="00:00" ,retention='7 days' ,format="{level}\t|{time:YY-MM-DD HH:mm:ss}\t|{file}\t|{line}\t|\t{message}")


def log(msg):
    time = datetime.datetime.now()
    print('[' + time.strftime('%Y.%m.%d-%H:%M:%S') + '] ' + msg)