# 线程测试
import math,time,random,sys,os
import concurrent.futures # 提供异步执行回调高层接口 
sys.path.append(os.path.abspath( os.path.join( os.path.dirname(__file__),".."))) #引入log所在绝对目录
import log

remark='''
submit:                         异步执行调用方法
                                调度可调用对象 fn,以 fn(*args, **kwargs) 方式执行并返回一个代表该可调用对象的执行的 Future 对象
map(func, *iterables, timeout=None, chunksize=1)
                                iterables 是立即执行而不是延迟执行的
                                func 是异步执行的，对 func 的多个调用可以并发执行
                                使用 ProcessPoolExecutor 时，这个方法会将 iterables 分割任务块并作为独立的任务并提交到执行池中。
                                这些块的大概数量可以由 chunksize 指定正整数设置 
                                chunksize 对 ThreadPoolExecutor 没有效果

shutdown(wait=True, *, cancel_futures=False)
                                当待执行的 future 对象完成执行后向执行者发送信号，它就会释放正在使用的任何资源
                                    关闭后调用 Executor.submit() 和 Executor.map() 将会引发 RuntimeError
                                wait:
                                    True    所有待执行的 future 对象完成执行且释放已分配的资源后才会返回
                                    False   方法立即返回，所有待执行的 future 对象完成执行后会释放已分配的资源
                                    无论何值，整个 Python 程序将等到所有待执行的 future 对象完成执行后才退出
                                cancel_futures
                                    True    此方法将取消所有执行器还未开始运行的挂起的 Future,已完成或正在运行的 Future 将不会被取消
                                使用 with 语句，可避免显式调用这个方法，它将会停止 Executor (就好像 Executor.shutdown() 调用时 wait 设为 True 一样等待):

Future:
    cancel()
        尝试取消调用,调用正在执行或已结束运行不能被取消则该方法将返回 False，否则调用会被取消并且该方法将返回 True
    cancelled()
        如果调用成功取消返回 True
    running()
    done()    
        已被取消 或 正常结束 返回 True
    result(timeout=None):
        返回调用返回的值,如果调用还没完成那么这个方法将等待 timeout 秒
                        如果在 timeout 秒内没有执行完成,触发 concurrent.futures.TimeoutError
                        没有指定或为 None,那么等待时间就没有限制
        futrue 在完成前被取消则 触发 CancelledError
        调用引发了一个异常，这个方法也会引发同样的异常
    exception(timeout=None)
        返回由调用引发的异常,timeout 参数与 result一致
        如果调用正常完成那么返回 None
    add_done_callback(fn)
        当 future 对象被取消或完成运行时，将会调用 fn(future) ,future 对象将作为它唯一的参数
        可调用对象 fn 总被属于添加它们的进程中的线程按加入的顺序调用，如果可调用对象fn 引发一个 Exception 子类，它会被记录下来并被忽略掉
                                                                 如果可调用对象引发一个 BaseException 子类，行为没有定义 
        如果 future 对象已经完成或已取消,fn 会被立即调用    

    wait(fs, timeout=None, return_when=ALL_COMPLETED)->{done:{down,canel},not_down:{}}
        等待由 fs 指定的 Future 实例（可能由不同的 Executor 实例创建）完成
                重复传给 fs 的 future 会被移除并将只返回一次
        返回一个由集合组成的具名 2 元组。 
                            第一个集合的名称为 done,包含在等待完成之前已完成的 future（包括正常结束或被取消的 future）
                            第二个集合的名称为 not_done，包含未完成的 future（包括挂起的或正在运行的 future）
        timeout :可以用来控制返回前最大的等待秒数
        return_when: 指定此函数应在何时返回,必须为以下常数之一  
            FIRST_COMPLETED     在任意可等待对象结束或取消时返回
            FIRST_EXCEPTION     任意可等待对象因引发异常而结束时返回 ,未引发任何异常时 === ALL_COMPLETED
            ALL_COMPLETED       函数将在所有可等待对象结束或取消时返回

    as_completed(fs, timeout=None)
        fs: 与 wait 一致, 在 as_completed() 被调用之前完成的 future 对象将优先被生成,
    如果 __next__() 被调用并且在对 as_completed() 的原始调用 timeout 秒之后结果仍不可用，则返回的迭代器将引发 concurrent.futures.TimeoutError

    Executor 实现调用或由单测试调用 调用的方法：
        set_running_or_notify_cancel():     只可以在执行关联 Future 工作之前由 Executor 实现调用或由单测试调用
                                            返回 False 那么 Future 已被取消，[即 Future.cancel() 已被调用并返回 True]
                                                等待 Future 完成 (即通过 as_completed() 或 wait()) 的线程将被唤醒
                                            这个方法只可以被调用一次并且不能在调用 Future.set_result() 或 Future.set_exception() 之后再调用


        set_result(result) :        将 Future 关联工作的结果给 result
        set_exception(exception) :   设置 Future 关联工作的结果给 Exception exception
        
'''
print(remark)

arr=[1] 
def sleep(i):
    leep= random.randrange(1,2)
    time.sleep(leep) 
def work(i):
    sleep(i)
    print(f"工作{i}...")
    if i==random.randrange(1,6):return False
    return True
def sqrt(i): 
    sleep(i)
    return math.sqrt(i)
def sum(i,j):
    sleep(i)
    return i+j 
log.start_mark("map")
executor=concurrent.futures.ThreadPoolExecutor(max_workers=2)
map=executor.map(sqrt,arr)  
for s,m in zip(arr,map):print(f"{s} 开方：{m}" )
log.end_mark("map")


log.start_mark("结果")
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as e:
    futureList=[e.submit(work,i ) for i in arr] 
    for future in concurrent.futures.as_completed(futureList):
        print(f"完成工作结果：{future.result()}")
log.end_mark("结果")
log.start_mark("参数——结果") 
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as e:
    futureDict={e.submit(sum,i,2):i for i in arr} 
    for future in concurrent.futures.as_completed(futureDict): 
        i=futureDict[future]
        print(f"{i}+2={future.result()}")
log.end_mark("参数——结果") 
log.start_mark("参数——结果wait") 

arr=[1,2,3,4,5,6,7,8,9,10,11,21]
executor=concurrent.futures.ThreadPoolExecutor(max_workers=3)
futureDict={executor.submit(sum,i,2):i for i in arr} 
for kv in futureDict.keys():
    i=futureDict[kv]
    if random.randrange(0,5)%2==0:
        r=kv.cancel()
        if  not r: log.warn(f"{i} 取消不成功")
        else:log.info(f"{i}取消成功")
    else:log.info(f"{i}正常执行")

log.info("*"*20)
ffDict=concurrent.futures.wait(futureDict,timeout=1) 
start = time.perf_counter()

for f in ffDict.done:
    i=futureDict[f]
    if f.cancelled(): log.warn(f"{i}执行被取消")
    else: print(f"{i}+2={f.result()}")
for f in ffDict.not_done:
    i=futureDict[f]
    #if f.cancelled():log.warn(f"被取消的Future{i}")
    if f.done() and not f.cancelled():
        end = time.perf_counter()
        log.warn(f"未完成的经过 { end - start}ms 又完成了{i}+2={f.result()}")
    else: log.warn(f"未完成的Future:{i},cancelled:{f.cancelled()}\tdone:{f.done()}\trunning:{f.running()}")
log.end_mark("参数——结果wait") 