import sys,os,json
import argparse
import htmlparser

#sys.path.append(os.path.dirname(os.path.abspath(sys.argv[0])+"../tool"))
from clashUtility import clash,clashOption
from co6co.utils import log
from co6co.utils.File import File
from co6co_clash import nodes as nodesParser

import concurrent.futures; 

def parse(item,proxy:str=None):
    try: 
        enabled=item["enabled"]
        if not enabled: return
        methodName=item["method"]  
        _,vmessList=htmlparser.HtmlParser.getParseContent(item,methodName) 
        #获取到的地址为Nul 不使用代理再尝试一次：
        if proxy !=None and ( vmessList ==None or (type(vmessList) == list and len(vmessList)==0)):_,vmessList=htmlparser.HtmlParser.getParseContent(item,methodName)
        return vmessList
    except Exception as e:
        log.err(item["remarks"]+"出错"+e)
        pass

def parseSubUrls(jsonFilePath,args:dict): 
    jsonObj=File.readJsonFile(jsonFilePath)

    clashOpt=clashOption([]) 
    clashOpt.outputPath=args.outputFolder
    clashOpt.backLocalTemplate=args.templateFile 
    c=clash (clashOpt) 
    template=c.templateConfig()

    with concurrent.futures.ThreadPoolExecutor(max_workers=1)  as executor:
        futures= {executor.submit(parse,item,args.proxy):item for item in jsonObj["data"] }
        for future  in concurrent.futures.as_completed(futures):
            try:
                item=futures[future]
                result=future.result()
                if result != None and len(result)>0:
                    nodes= nodesParser.parser(result) 
                    log.start_mark("remove")
                    nodes=clash.remove_duplicates(nodes)
                    log.end_mark("remove")
                    if args.checknode: 
                        log.start_mark(f"check Node {len(nodes)}...")
                        nodes=clash.checkNodes(nodes,args.delay) 
                        log.start_mark(f"check Node {len(nodes)}.")
                    c.outputToFile(template,nodes,3000,args.outputFolder,f"3_{item['id']}.yaml") 
            except Exception as e:
                log.err(f"parseSubUrls err",e)
                raise

if __name__ == '__main__': 
    default_output_dir=os.path.join(os.path.abspath("."),"sub",'yaml') 
    default_config_dir=os.path.join(os.path.abspath("."),"file") 
     
    parser=argparse.ArgumentParser(description="生成clash Yaml文件")
    parser.add_argument("-p","--proxy",help="config proxy address eg. 127.0.0.1:1080")

    config=parser.add_argument_group("config") 
    config.add_argument("-c",'--subConfigFile' , help=f"sub Config JSON File Path,default:\"{ os.path.join(default_config_dir,'subUrl2.json')}\"",default= os.path.join(default_config_dir,"subUrl2.json"))
    config.add_argument("-t","--templateFile",help=f"standby clash yaml templcate File,default:\"{os.path.join(default_config_dir,'clashConfigTemplate.yaml')}\"",default=os.path.join(default_config_dir,"clashConfigTemplate.yaml"))
    
    config=parser.add_argument_group("filter")
    config.add_argument("-d","--delay",  help="node delay within xx ms,default 1000ms ", type=int, default=1000) 
    config.add_argument('--checknode', default=True, action=argparse.BooleanOptionalAction ,help="check network connect and check port")


    config=parser.add_argument_group("output")
    config.add_argument("-n","--number",  help="node num per yaml,default 150", type=int, default=150)
    config.add_argument("-o",'--outputFolder' , help=f"save yaml file Path,defalut:{default_output_dir}",default=default_output_dir)
    
 
    args=parser.parse_args()
    log.start_mark("解析") 
    jsonData=parseSubUrls(args.subConfigFile,args)
    log.end_mark("解析") 
    
