import requests,base64,sys
sys.path.append("./tool")
from webutility import safe_decode
from co6co.utils import log
from co6co.utils.http import get
import tcp
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
delay=tcp.ping("www.baidu.com") # 在github Action 不支持
log.info(f"检测网络延迟：{'www.google.com'}: {delay} ms")

 
try:
    response = get('https://raw.githubusercontent.com/zhangkaiitugithub/passcro/main/speednodes.yaml')  
    #print("Encoding:"+response.apparent_encoding,response.encoding)
    response.encoding="utf-8"
    print(response.text )
except Exception as e:
    log.err(f"[-]http请求'{url}'出现异常：{e}",e)
    pass
