import sys,os,json
import argparse
import htmlparser
from clashUtility import clash,clashOption, log,resourceType,nodeResource
sys.path.append(os.path.dirname(os.path.abspath(sys.argv[0])+"../tool"))

import concurrent.futures;
def readFile(filePath):
    '''
    filePath: 文件路径\n
    return list 
    '''
    file=open(filePath,"r",encoding='utf-8') 
    urls=file.read().splitlines()# readlines() 会存在\n
    return urls
def readJsonFile(filePath):
    '''
    filePath: 文件路径\n
    return     json 
    '''
    with  open(filePath,"r",encoding='utf-8') as f:
        result=json.load(f) 
        return result

def writeJsonFile(filePath,obj):
    '''
    filePath: 文件路径\n
    return     json 
    '''
    updated_list = json.dumps( obj, sort_keys=False, indent=2, ensure_ascii=False)
    file = open(filePath, 'w', encoding='utf-8')
    file.write(updated_list)
    file.close()

def parse(item,proxy:str=None):
    try:
        enabled=item["enabled"]
        if not enabled: return
        methodName=item["method"] 
        #log("'%s' 调用方法：%s"%(item["remarks"],htmlparser.__dict__.get(methodName)))
        invokeMethod=htmlparser.__dict__.get(methodName)
        if invokeMethod== None: return

        url=invokeMethod(item,proxy)
        #获取到的地址为Nul 不使用代理再尝试一次：
        if proxy !=None and ( url ==None or (type(url) == list and len(url)==0)):url=invokeMethod(item)
        #log.info(f"[+]解析后URL为:{url}")
        if type(url) == list:
            urls=url
            if len(urls)>0:item["url"]="|".join(urls)
        else:
            if url!=None and url !="":item["url"]=url
    except Exception as e:
        log.err(item["remarks"]+"出错"+e)

def parseSubUrls(jsonFilePath,proxy:str=None): 
    jsonObj=readJsonFile(jsonFilePath)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4)  as executor:
        futures= {executor.submit(parse,item,proxy) for item in jsonObj["data"] }
    concurrent.futures.wait(futures,return_when=concurrent.futures.FIRST_COMPLETED)
    writeJsonFile(jsonFilePath,jsonObj)
    return jsonObj 
 
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
    log.info(f"\r\n{'--'*30}>")
    log.info("解析订阅的url...")  
    jsonData=parseSubUrls(args.subConfigFile,args.proxy)
    urlData=[{"id":item["id"],"data":item["url"].split("|")} for item in jsonData["data"] if item['enabled']]
 
    nodeResources =[] # [nodeResource(str(item["id"]),resourceType.http,u) for item in urlData for u in item["data"] if u!=""]
    for item in urlData:
        for u in item['data']:
            nodeResources.append(nodeResource(str(item["id"]),resourceType.http,u))
   
    log.info(f"[+] 解析后订阅资源数：{len(nodeResources)}") 
    log.info(f"\r\n<{'=='*30}\r\n\r\n")
    sys.exit(0)

    #clashOpt=clashOption([nodeResources[1]])
    clashOpt=clashOption(nodeResources)
    clashOpt.checkNode=args.checknode
    clashOpt.outputPath=args.outputFolder
    clashOpt.backLocalTemplate=args.templateFile
    clashOpt.delay=args.delay
    clashOpt.proxy=args.proxy
    clashOpt.nodeOutputToFile=args.nodeOutputTxt
    c=clash (clashOpt)
    c.genYamlForClash(args.number)
