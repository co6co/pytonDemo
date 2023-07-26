import argparse
import os,sys,re,time
from typing import List 
from log import *
from tcp import *
import concurrent.futures as futures

class PingService:
    ipDict=None #{"127.0.0.1":300}
    def __init__(self,ips:list) -> None:
        self.ipDict={ip:3000 for ip in ips if re.search("(\d{1,3}.){3}\d{1,3}",ip) !=None }
        pass

    def pings(self):
        executor=futures.ThreadPoolExecutor(max_workers=4) 
        futureDict={executor.submit(ping,ip):ip  for ip in self.ipDict}
        for future in futures.as_completed(futureDict):
            ip=futureDict[future] 
            result=future.result() 
            old_result=self.ipDict[ip] 
            self.ipDict[ip] =result
            # 两者不同 表示 表示网络发生变化 
            #  
            info(f"检测结果：{ip}\t{old_result}->{result}\t 不打印在日志。")
            if None in [result,old_result] and int in [type(result),type(old_result)]:
                logger.info(f"{ip}网络发生变化\t{old_result}->{result}")
        executor.shutdown()


def readFile(filePath:str)->List[str]|None:
    file=None
    try:
        if not os.path.exists(filePath):
            file=open(filePath,"w",encoding="utf-8")
            file.write("127.0.0.1\n")
            file.seek(0)
        else:
            file=open(filePath,"r",encoding="utf-8")
        ips=file.read().splitlines()# readlines() 会存在\n
        return ips
    except Exception as e:
        err(f"read File error:{e}")
        pass
    finally:
        if file !=None:
            file.close()
def main():
    currentFolder=os.path.abspath(".") 
    parser=argparse.ArgumentParser(description="检测目标是否一致通")
    parser.add_argument("-f","--file",help="ip 所在的文本",default=os.path.join(currentFolder,"ips.txt"))
    parser.add_argument("-s","--sleep",help="休息时间 s", type=int, default=60)
    args=parser.parse_args()

    ips=readFile(args.file)
    if ips !=None: 
        srv=PingService(ips)
        while(True): 
            srv.pings()
            time.sleep(args.sleep)
            
     
    

if __name__ =="__main__":main()