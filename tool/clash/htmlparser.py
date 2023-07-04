import urllib.parse,datetime
from bs4 import BeautifulSoup
import re,sys
sys.path.append("./tool")
import log,webutility


def _createSoup(url):
    response=webutility.get(url) 
    #https://www.jianshu.com/p/424e037c5dd8
    soup=BeautifulSoup(response.text,"html.parser") #html5lib
    return soup

  
def kauiZuiKeji(item):
    def getSubUrl(href,arg):
        log.info("嘴科技地址为："+href)
        soup=_createSoup(href) 
        ps=soup.select("p")
        for p in ps:
            if p.string:
                reg=arg #"https://tt.vg/\w+"
                m=re.search(reg,p.string)
                if m:
                    #print(f"{m.group()}")
                    log.succ("[+]订阅地址："+m.group())
                    return m.group()
    url=item["site"]
    arg1=item["arg_1"]
    arg2=item["arg_2"]
    arg3=item["arg_3"]
    name=item['remarks'] if  'remarks' in item else "未配置remarks"
    log.info(f"解析'{name}'的订阅地址..{arg1}\t{arg2}\t{arg3}.") 
    soup=_createSoup(url)  
    list=soup.select(arg1)#'a[href*="https://kkzui.com/"]'
    for item in list:
        ret=arg2#"https://kkzui.com/\d+.html"
        m=re.search(ret,item["href"])
        if m:
            url=item["href"]
            return getSubUrl(url,arg3)
    return None

def getHubDateTime(item):
    url=item["site"]
    arg1=item["arg_1"]
    arg2=int(item["arg_2"])
    arg3=item["arg_3"]
    name=item['remarks'] if  'remarks' in item else "未配置remarks"
    soup=_createSoup(url) 
    f=soup.find("include-fragment")
  
    f=soup.find_all(attrs={"src":True})
    urlparse=urllib.parse.urlparse(url)
    url=None
    
    for i in f:
        if i.name=='include-fragment':
            if 'master' in i['src']:url=f"{urlparse.scheme}://{urlparse.netloc}{i['src']}"
    if url ==None:
        log.err("url is Null")
        url= item["site"].replace("tree","file-list")
    log.info("请求URL:"+url)
    soup=_createSoup(url)  
    list=soup.select(arg1)
    
    dateRet="\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}"
    urlArr=[]
    for a in list: 
        search=re.search(dateRet,a.getText())
        if  search!=None:
            delay=datetime.timedelta(seconds=arg2)
            now=datetime.datetime.now()
            updateTime=datetime.datetime.fromisoformat(search.group(0))
            if now > updateTime.__add__(delay):
                log.warn(f"过期：{now-updateTime} 超过`{arg2}s` ")
                continue 
            #log.err(type(a.parent.parent.previous_sibling))
            #log.err( f"{type(a.parent.parent)}{a.parent.parent['role']}{a.parent.parent['class']}")
            px=a.parent.parent.parent.findChild("a",attrs={"class":"Link--primary"})
            if px == None:continue
            #print(type(px)) #<class 'bs4.element.Tag'>
            # todo why not use previous_sibling
            #px=a.parent.parent.previous_sibling  #<class 'bs4.element.NavigableString'>
            path=px["href"]
            log.succ(path)
            #https://github.com/mahdibland/V2RayAggregator/blob/master/sub/list/61.txt
            #https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/list/61.txt
            path=path.replace("blob/","")
            urlArr.append(f"https://raw.githubusercontent.com{path}") 
    #if len(urlArr)>0:item["url"]="|".join(urlArr)
    return urlArr


if __name__ == "__main__":
    #url=kauiZuiKeji({"site":"https://kkzui.com/#term-6","arg_1":"a[href*=\"https://kkzui.com/\"]","arg_2":"https://kkzui.com/\\d+.html","arg_3":"https://tt.vg/\\w+"})
    item={"site":"https://github.com/mahdibland/V2RayAggregator/tree/master/sub/list","arg_1":".Link--secondary","arg_2":"86400","arg_3":"https://tt.vg/\\w+"}
    url=getHubDateTime(item)
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
