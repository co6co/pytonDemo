import requests,base64,sys,os
from co6co.utils import log
from co6co.utils.http import get

log.err(f'CWD:\t{os.getcwd()}')
log.info(f"__file__\t{__file__}")
log.warn(f"path:{sys.path[0:5]}...")

log.succ('''
总结：
    1.sys.path 中的相对路径是： os.getcwd() 的相对路径
    2.sys.path 中不一定包含    os.getcwd()
''')
'''
from ..webutility import safe_decode
'''
sys.path.append("./tool")
log.warn(f"path:{sys.path}...")
from webutility import safe_decode
import  tcp


try:
    url="https://raw.fastgit.org/Pawdroid/Free-servers/main/sub"
    headers=   {"User-agent":"'Mozilla/5.0 (X11; U; Linux 2.4.2-2 i586;en-US; m18) Gecko/20010131 Netscape6/6.01"}
    response=requests.get(url, headers=headers, timeout=3000)
    raw = base64.b64decode(response.text)
    nodes=raw.splitlines() 
    saft_code="YWVzLTI1Ni1nY206UENubkg2U1FTbmZvUzI3"
    print( safe_decode(saft_code).decode('utf-8'))
except:
    pass
delay=tcp.ping("www.baidu.com")
log.info(f"检测网络延迟：{'www.google.com'}: {delay} ms")

 
try:
    response = get('https://raw.githubusercontent.com/zhangkaiitugithub/passcro/main/speednodes.yaml')  
    #print("Encoding:"+response.apparent_encoding,response.encoding)
    response.encoding="utf-8"
    log.info('f"https://raw.githubusercontent.com/zhangkaiitugithub/passcro/main/speednodes.yaml":{response.status_code}' )
except Exception as e:
    log.err(f"[-]http请求'{url}'出现异常：{e}",e)
    pass
