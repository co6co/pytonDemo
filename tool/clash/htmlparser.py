import requests
from bs4 import BeautifulSoup
import re

def _createSoup(url):
    response=requests.get(url,allow_redirects=True) 
    soup=BeautifulSoup(response.text) 
    return soup
def getUrl(): 
    soup=_createSoup("https://kkzui.com/#term-6")  
    list=soup.select('a[href*="https://kkzui.com/"]')
    for item in list:
        ret="https://kkzui.com/\d+.html"
        m=re.search(ret,item["href"])
        if m: 
            return item["href"]
        
    return None

def getSubUrl(href):
    soup=_createSoup(href) 
    ps=soup.select("p")
    for p in ps:
        if p.string:
            reg="https://tt.vg/\w+"
            m=re.search(reg,p.string)
            if m:
                #print(f"{m.group()}")
                return m.group()
                  
    
if __name__ == "__main__":
    url=getUrl()
    sub=getSubUrl(url)

    target=f"G:\Tool\SHARE\yaml\cp\subUrl.txt" 
    f=open(target,"r+",encoding="utf-8")
    allSub=f.read().splitlines()
    if sub not in allSub:
        allSub.append(sub)
        
    f.seek(0)
    f.truncate()#      
    content="\n".join(allSub)
    print(content)
    f.write(content)
    f.close()
