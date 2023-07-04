import math,sys,os
#from .tool import log
print(os.path.abspath( os.path.join( os.path.dirname(__file__),"./tool")))
sys.path.append(os.path.abspath( os.path.join( os.path.dirname(__file__),"./tool"))) #引入log所在绝对目录
import log

print("asdf\033[5;31;40mtestast\033[0m!\n12346\n456asdf")
print("\033[1;31;46;1m Hallo World \033[m")

def test(ab:str,*args,**kwargs):
    log.warn(ab)
    log.warn(type(args))

    for v in args:
      print ('(args): ', v)
    
    log.err(type(kwargs))
    for k, v in kwargs.items():
      print ('abc %s: %s' % (k, v))
      
test("abc",123,1, k1=5, k2=6)
