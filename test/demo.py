
'''
Python 的内部工作原理不允许你做相对导入
除非你指定了所有模块所在的顶级目录。
通过在运行主脚本时添加项目的根目录，可以解决相对导入错误。
'''
 
'''
程序入口运行的模块为主模块， name == "__mian__"

当程序入口为当前目录，根目录就是当前目录， .. 是找不到父目录的
'''
print ('当前名称：',__name__)
from .. import root
r=root()
r.print()

from .dmodel import  d as dClass
d=dClass()
d.p()
from ..tool.log import info

info("seccess")

def main():
    print(333)
