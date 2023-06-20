import os ,sys,time
from loguru import logger
logger.remove()
logger.add(sys.stdout,level="INFO",format="{message}")
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

logger.add("c:\log\python\loguru_{time:YY-MM-DD_HH}_INFO.log",level="INFO",encoding="utf-8" ,rotation="00:00" ,retention='7 days' ,format="{level}|{time:YY-MM-DD HH:mm:ss}|{file}|{line}|\t{message}")
logger.add("c:\log\python\loguru_{time:YY-MM-DD_HH}_ERROR.log",level="ERROR",encoding="utf-8" ,rotation="00:00" ,retention='7 days' ,format="{level}|{time:YY-MM-DD HH:mm:ss}|{file}|{line}|\t{message}")

class Command: # 执行windows 命令
    def __init__(self,commandText:str,resultContain=str|None) -> None: 
        if not isinstance(commandText,str):
            sys.exit(0)
        self.commandText=commandText
        self.contain=resultContain
    def exec(self):
         
        result= self.execReturnText()
        #print(f"执行命令：{self.commandText}\n结果：\n{result}")
        return True if self.contain in  result else False
    def execReturnText(self):
        '''
        #执行命令的另一种方式
        result=os.system("sc query AppManagement")
        '''
        p=os.popen( self.commandText)
        result=  p.read()
        return result

class Protection: #守护程序 
    def __init__(self,checkCommand:Command,successCommand:Command|None,failCommand:Command|None) -> None:
        self.checkCommand=checkCommand
        self.successCommand=successCommand
        self.failCommand=failCommand
        pass
    def check(self):
         if not isinstance(self.checkCommand,Command):
            logger.info("不支持的命令对象")
            exit(0)
         elif self.checkCommand.contain == None:
            logger.info("必须有contain 属性")
            exit(0)
         checkResult=self.checkCommand.exec()
         if checkResult and self.successCommand !=None:
            logger.info(f"检测成功...执行命令。{self.successCommand.exec()}")
         elif not checkResult and self.failCommand !=None:
            logger.info(f"检测失败...执行命令：{ self.failCommand.exec()}")
         else:
            logger.info(f"检测结果：{checkResult}")