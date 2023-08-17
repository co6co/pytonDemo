import os,sys  
print("__file__",__file__) #当前文件所在目录
print("__name__",__name__) #python 运行 所在目录

currentFolder=os.path.dirname(__file__)
logDir=os.path.abspath(os.path.join(currentFolder,".."))
#print(f"curdir:{os.path.curdir},{__file__}") 
print(f"sys.argv:\t{sys.argv}\n__file__:\t{__file__},\n{os.path.dirname(__file__)}")
sys.path.append(logDir)
import co6co.utils.log as log
log.log("123456")
currentFilePath=os.path.abspath(sys.argv[0])
print(f"当前文件路径：{currentFilePath}\n当前文件目录：{os.path.dirname(currentFilePath)}")


import requests
proxies = {
   'http': 'http://127.0.0.1:9666',
   'https': 'https://127.0.0.1:9666'
}

headers={
'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'zh-CN,zh;q=0.9',
'referer':'https://tt.vg/evIzX',
#'cookie': 'PHPSESSID=ep1kk1sl39t3lbgjh8qb1r2mc0; short_77706=1',
#'referer': 'https://item-paimai.taobao.com/pmp_item/609160317276.htm?s=pmp_detail&spm=a213x.7340941.2001.61.1aec2cb6RKlKoy',
##'sec-fetch-mode': 'cors',
#"sec-fetch-site": 'same-origin',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
#'x-requested-with': 'XMLHttpRequest' 
}
headers={
    #"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    #"Accept-Encoding":"gzip, deflate, br",
    #"Accept-Language":"zh-CN,zh;q=0.9",
    #"Cache-Control":"no-cache",
    #"Pragma":"no-cache",
    #"Sec-Ch-Ua":'"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    #"Sec-Ch-Ua-Mobile":"?0",
    #"Sec-Ch-Ua-Platform":'"Windows"',
    #"Sec-Fetch-Dest":"document",
    #"Sec-Fetch-Mode":"navigate",
    #"Sec-Fetch-Site":"none",
    #"Sec-Fetch-User":"?1",
    #"Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    #'User-Agent':'BaiduSipder'
}
'''
try:
    res=requests.get("https://oss.v2rayse.com/proxies/data/2023-06-20/TS49Gwj.txt",headers=headers,timeout=(15, 30),proxies=proxies)
    print(res.text)
except Exception as e:
    print(e)
'''
resp = requests.get("https://tt.vg/evIzX",headers=headers, timeout=(15, 30),allow_redirects=True,proxies=proxies)
if len(resp.history) > 0:
    location_url = resp.history[len(resp.history) - 1].headers.get('Location')
    resp=requests.get(location_url,headers=headers,timeout=(15, 30),proxies=proxies)
    print(resp.text)