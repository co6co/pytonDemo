# 线程测试
import math
import concurrent.futures

arr=[1,2,3,4,5]

def sum(i,j):
    return i+j

print('实例1.。。。。。。。。。。。。。。。。')
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as e:
    sfutures=[]
    for i in arr:
      sfutures.append(  e.submit(sum,i,3))
    print(f"type:{type(sfutures)}")

    for future in concurrent.futures.as_completed(sfutures):
        print(f" 未知+3={future.result()}")

print('实例1.。。。。。。。。。。。。。。。。')    
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as e:
    sfutures={e.submit(sum,i,2):i for i in arr}
    print(f"type:{type(sfutures)}") 
    for future in concurrent.futures.as_completed(sfutures):
        print(f'future:{future},{type(future)}')

        i=sfutures[future]
        print(f"{i}+2={future.result()}")


