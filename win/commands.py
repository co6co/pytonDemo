import os ,sys,time
#print("log 所在目录：{}\tsys.path.append 是否需要用全路径".format(os.path.abspath( os.path.join(os.path.dirname(__file__),"../tool") )))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),"../tool") ))
sys.path.append("../tool")
from log import *
 
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