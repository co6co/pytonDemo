
import os,sys
sys.path.append(os.path.join(os.path.dirname(__file__),"../tool"))
import log
def test_tuple(ars=()):
    log.warn(f"ars=() 参数类型：{type(ars)}") 
    log.info("值：")
    for v in ars:
      print (v)
   
def sigalStar0(ab:str,*,kwargs):
   '''
    * 后面的参数只能使用 关键字参数
   '''
   log.info(kwargs)
   log.info(ab)
def sigalStar(*args):
    log.warn(f"*args 参数类型：{type(args)}") 
    log.info("值：")
    for v in args:
      print (v)
   
def doubleStar( **kwargs): 
    log.warn(f"**kwargs 参数类型：{type(kwargs)}") 
    log.info("值：")
    for k, v in kwargs.items():
      print ('abc %s: %s' % (k, v))
      

test_tuple([1])
sigalStar0("456asdf",kwargs=23)
sigalStar("abc",(123,),1,2,3,4)
sigalStar(("abc",(123,),1,2,3,4))
sigalStar(*("abc",(123,),1,2,3,4))
doubleStar(  k1=5, k2=6)
doubleStar(**{"k1":5, "k2":6})