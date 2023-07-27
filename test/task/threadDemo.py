import threading,sys,os,time
sys.path.insert(1,os.path.abspath(os.path.join(os.path.dirname(__file__),"../../tool") ))
import log

def run(name:str,s:int=30)->None:    
    log.info(f"{name}")
    time.sleep(s)
    log.info(f"{name} .{s}s exit ")
    
def main():
    '''
    总计线程：
    join: 需要等待线程结束才继续
    setDaemo: 将线程设为守护线程[主线程退出, 守护线程也退出]
    run: 可理解为 start 和 join 的功能合一
    '''
    t=threading.Thread(target=run,args=("线程1",5,))
    t.setDaemon(True) # 设置了守护父进程退出 守护线程也退出
    #t.run()# 卡住，线程不完程序不走
    t.start()
    #t.join() # 卡住 等待子线程执行完，
             #不存在该语句，子线程仍旧执行，只是
    t2=threading.Thread(target=run,args=("线程2",10,))
    t2.start()
    t2.join() # 主线程等待T2 执行完就退出
    #t.join()

 
if __name__ == "__main__":
    log.info("main Thread.")
    main()
    log.info("main exit")
    