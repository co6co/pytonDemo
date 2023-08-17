import sys,os,json
import argparse
import htmlparser
from clashUtility import clash, clashOption, resourceType, nodeResource

import concurrent.futures
from co6co.utils import log
from co6co.utils.File import File


def parse(item,proxy:str=None):
    try:
        enabled=item["enabled"]
        if not enabled: return
        methodName=item["method"]  
        url,_=htmlparser.HtmlParser.getParseContent(item,methodName) 
        #获取到的地址为Nul 不使用代理再尝试一次：
        if proxy !=None and ( url ==None or (type(url) == list and len(url)==0)):url,_=htmlparser.HtmlParser.getParseContent(item,methodName)
        
        #log.info(f"[+]解析后URL为:{url}")
        if type(url) == list:
            urls=url
            if len(urls)>0:item["url"]="|".join(urls)
        else:
            if url!=None and url !="":item["url"]=url
    except Exception as e:
        log.err(item["remarks"]+"出错"+e)

def parseSubUrls(jsonFilePath,proxy:str=None): 
    jsonObj=File.readJsonFile(jsonFilePath)
    with concurrent.futures.ThreadPoolExecutor(max_workers=1)  as executor:
        futures= {executor.submit(parse,item,proxy) for item in jsonObj["data"] }
    concurrent.futures.wait(futures,return_when=concurrent.futures.FIRST_COMPLETED)
    File.writeJsonFile(jsonFilePath,jsonObj)
    return jsonObj 

def revisedResource(configJson:dict):
    '''
    获取资源
    配置文件设计时：采用一个订阅 可订阅多个资源
    在系统中将所有资源分开,ID不可重复.
    '''
    urlData=[{"id":item["id"],"data":item["url"].split("|")} for item in configJson["data"] if item['enabled']] 
    nodeResources = [nodeResource(item["id"],resourceType.http,u) for item in urlData for u in item["data"] if u!=""]
    
    # id 转 唯一
    ids=[]
    for r in nodeResources:
        if r.id not in ids:ids.append(r.id)
    for id in ids:
        i=0
        for r in nodeResources:
            if id==r.id:
                r.id=int(str(r.id)+f"{i:0>3d}")
                i+=1
    return nodeResources

if __name__ == '__main__': 
    default_output_dir=os.path.join(os.path.abspath("."),"sub")
    default_config_dir=os.path.join(os.path.abspath("."),"file") 
     
    parser=argparse.ArgumentParser(description="生成clash Yaml文件")
    parser.add_argument("-p","--proxy",help="config proxy address eg. 127.0.0.1:1080")

    config=parser.add_argument_group("config") 
    config.add_argument("-c",'--subConfigFile' , help=f"sub Config JSON File Path,default:\"{ os.path.join(default_config_dir,'subUrl.json')}\"",default= os.path.join(default_config_dir,"subUrl.json"))
    config.add_argument("-t","--templateFile",help=f"standby clash yaml templcate File,default:\"{os.path.join(default_config_dir,'clashConfigTemplate.yaml')}\"",default=os.path.join(default_config_dir,"clashConfigTemplate.yaml"))
    
    config=parser.add_argument_group("filter")
    config.add_argument("-d","--delay",  help="node delay within xx ms,default 1000ms ", type=int, default=1000) 
    config.add_argument('--checknode', default=True, action=argparse.BooleanOptionalAction ,help="check network connect and check port")


    config=parser.add_argument_group("output")
    config.add_argument("-n","--number",  help="node num per yaml,default 150", type=int, default=150)
    config.add_argument("-o",'--outputFolder' , help=f"save yaml file Path,defalut:{default_output_dir}",default=default_output_dir)
    config.add_argument('--nodeOutputTxt' ,default=True, action=argparse.BooleanOptionalAction,help=f"nodes to File default:true")
 
    args=parser.parse_args()
    log.start_mark("解析")
    log.info("解析订阅的urls...")  
    jsonData=parseSubUrls(args.subConfigFile,args.proxy)
    nodeResources=revisedResource(jsonData)
    log.info(f"[+] 解析后订阅资源数：{len(nodeResources)}") 
    log.end_mark("解析")
    #clashOpt=clashOption([nodeResources[1]]) 
    clashOpt= clashOption(nodeResources)
    clashOpt.checkNode=args.checknode
    clashOpt.outputPath=args.outputFolder
    clashOpt.backLocalTemplate=args.templateFile
    clashOpt.delay=args.delay
    clashOpt.proxy=args.proxy
    clashOpt.nodeOutputToFile=args.nodeOutputTxt
    c=clash (clashOpt) 
    c.genYamlForClash(args.number) 
