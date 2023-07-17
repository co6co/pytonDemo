import urllib.parse,datetime,pytz
from bs4 import BeautifulSoup
import re,sys
sys.path.append("./tool")
import log,webutility


def _createSoup(url,proxy:str=None): 
    response=webutility.get(url,proxy=proxy) 
    #https://www.jianshu.com/p/424e037c5dd8
    soup=BeautifulSoup(response.text,"html.parser") #html5lib
    return soup

  
def kauiZuiKeji(item,proxy:str=None):
    '''
    三步获取订阅URL

    item["site"]    : 主页URL
    item["arg_1"]   : 获取页面元素
    item["arg_2"]   : 匹配 包含订阅页面 的URL
    item["arg_3"]   : 匹配 订阅URL
    '''
    def getSubUrl(href,arg): 
        soup=_createSoup(href,proxy)  
        ps=soup.select("p")
        for p in ps:
            if p.string:
                reg=arg #"https://tt.vg/\w+"
                m=re.search(reg,p.string)
                if m:
                    url=m.group()
                    log.succ(f"3.'{name}'通过参数3,获取包含目标URL..{url}") 
                    return url
        return None
    try:
        url=item["site"]
        arg1=item["arg_1"]
        arg2=item["arg_2"]
        arg3=item["arg_3"]
        name=item['remarks'] if  'remarks' in item else "未配置remarks" 
        log.info(f"解析：{name}\t'{url}'")
        soup=_createSoup(url,proxy) 
        log.info(f"1.'{name}'通过参数1,获取包含目标的页面元素..")
        list=soup.select(arg1)#'a[href*="https://kkzui.com/"]'
        for item in list:
            m=re.search(arg2,item["href"])#"https://kkzui.com/\d+.html"
            if m:
                url=item["href"]
                log.info(f"2.'{name}'通过参数2,获取包含目标的页面URL..{url}")
                result=getSubUrl(url,arg3)
                if result!=None:return [result]
        return None
    except Exception as e:
        log.err(f"{name}出错：{e}")
        pass
    return None


def getHubDateTime(item,proxy:str=None):
    '''
    匹配 github.com 中最近更新
    item["arg_1"]       包含时间日期的匹配 2023-07-05 13:12:00
    item["arg_2"]       int 当前时间前多少s
    item["arg_3"]       未使用
    return 未过期 的订阅URL
    '''
    urlArr=[]
    try:
        url=item["site"]
      
        arg1=item["arg_1"]
        arg2=int(item["arg_2"])
        arg3=item["arg_3"]
        name=item['remarks'] if  'remarks' in item else "未配置remarks" 
        log.info(f"解析：{name}\t'{url}'")
        urlparse=urllib.parse.urlparse(url) 
        soup=_createSoup(url,proxy) 
        list=soup.select(arg1)
        #2023-07-05T11:42:59+08:00
        dateRet="\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+\d{2}:\d{2}"
       
        dirArr=[]
        for a in list:
            if a["datetime"] ==None:continue
            search=re.search(dateRet,a["datetime"])
            if  search!=None:
                delay=datetime.timedelta(seconds=arg2) 
                now=datetime.datetime.now().astimezone(pytz.timezone("Asia/Shanghai"))
                updateTime=datetime.datetime.fromisoformat(search.group(0))
                addUpdateTime= updateTime.__add__(delay)
                # offset-naive是不含时区的类型，而offset-aware是有时区类型，两者自然不能比较
                if now >addUpdateTime:
                    log.warn(f"过期：{now-updateTime} 超过`{arg2}s` ")
                    continue 
                px=a.parent.parent.findChild("a",attrs={"class":"Link--primary"})
                #是文件还是文件夹 
                svg=a.parent.parent.findChild("svg")
                if px == None or svg ==None:continue  
                type=svg["aria-label"]
                path=px["href"]
                if type=="Directory":
                    log.info(f"{path} is {type}")
                    dirArr.append(f"{urlparse.scheme}://{urlparse.netloc}{path}")
                    continue
                #else:"File"
                log.info(f"{path} is {type}")
                #print(type(px)) #<class 'bs4.element.Tag'>
                # todo why not use previous_sibling
                #px=a.parent.parent.previous_sibling  #<class 'bs4.element.NavigableString'> 
                log.succ(path)
                #https://github.com/mahdibland/V2RayAggregator/blob/master/sub/list/61.txt
                #https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/list/61.txt
                path=path.replace("blob/","")
                urlArr.append(f"https://raw.githubusercontent.com{path}")
        if len(dirArr)>0:
            for url in dirArr:
                log.info(f"请求子文件夹...{url}")
                itemTmp=item.copy()
                itemTmp["site"]=url
                tmp=getHubDateTime(itemTmp)
                if len(tmp)>0:urlArr.extend(tmp)
    except Exception as e:
        log.err(f"{url},err:{e}")
        pass
    return urlArr


if __name__ == "__main__":
    url=""
    url=kauiZuiKeji({"proxy":"127.0.0.1:9666", "site":"https://kkzui.com/#term-6","arg_1":"a[href*=\"https://kkzui.com/\"]","arg_2":"https://kkzui.com/\\d+.html","arg_3":"https://tt.vg/\\w+"})
    item={"site":"https://github.com/mahdibland/V2RayAggregator/tree/master/sub/list","arg_1":"relative-time[datetime]","arg_2":"86400","arg_3":""}
    #url=getHubDateTime(item)
    print(url)
    log.err("*"*100)
    item={"site":"https://github.com/zhangkaiitugithub/passcro","arg_1":"relative-time[datetime]","arg_2":"86400","arg_3":""}
    url=getHubDateTime(item)
    print(url)

    log.err("-"*100)
    item={"site":"https://github.com/mahdibland/V2RayAggregator","arg_1":"relative-time[datetime]","arg_2":"86400","arg_3":""}
    #url=getHubDateTime(item)
    print(url)


    
    sys.exit(0)
    target=f"G:\Tool\SHARE\yaml\cp\subUrl.txt"
    log(f"将订阅地址附加到指定文件。{target}")
   
    f=open(target,"r+",encoding="utf-8")
    allSub=f.read().splitlines()
    if url not in allSub:allSub.append(url)
        
    f.seek(0)
    f.truncate()
    content="\n".join(allSub)
    f.write(content)
    f.close()
