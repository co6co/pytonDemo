import argparse
import os,sys
from clashUtility import log,clashOption,clash,nodeResource,resourceType
from typing  import List


def revisedResource(urls)->List[nodeResource] :
    nodeResources =  [nodeResource(i,resourceType.http,url) for i,url in enumerate(urls)  if url!=""]
    return nodeResources
    

if __name__ == '__main__': 
    default_output_dir=os.path.join(os.path.abspath("."),"sub",'yaml') 
    default_config_dir=os.path.join(os.path.abspath("."),"file") 
    parser=argparse.ArgumentParser(description="生成clash Yaml文件")
    parser.add_argument("-p","--proxy",help="config proxy address eg. 127.0.0.1:1080") 
   
    config=parser.add_argument_group("config") 
    parser.add_argument("-u","--urls",help="订阅的URL,多个用 '|'分割") 
    config.add_argument("-t","--templateFile",help=f"standby clash yaml templcate File,default:\"{os.path.join(default_config_dir,'clashConfigTemplate.yaml')}\"",default=os.path.join(default_config_dir,"clashConfigTemplate.yaml"))

     

    
    config=parser.add_argument_group("filter")
    config.add_argument("-d","--delay",  help="node delay within xx ms,default 1000ms ", type=int, default=1000) 
    config.add_argument('--checknode', default=True, action=argparse.BooleanOptionalAction ,help="check network connect and check port")
    
    

    config=parser.add_argument_group("output")
    config.add_argument("-o",'--outputFolder' , help=f"save yaml file Path,defalut:{default_output_dir}",default=default_output_dir)

    args=parser.parse_args()
    log.start_mark("解析")
    log.info("解析订阅的urls...") 
    if args .urls ==None or args.urls =="":
        log.critical("参数 urls 未配置")
        sys.exit(0)

    urlsArray=args.urls.split("|")
    nodeResources=revisedResource(urlsArray)
    log.info(f"[+] 解析后订阅资源数：{len(nodeResources)}") 
    log.end_mark("解析")
    #clashOpt=clashOption([nodeResources[1]])
    clashOpt=clashOption(nodeResources)
    clashOpt.checkNode=args.checknode
    clashOpt.outputPath=args.outputFolder
    clashOpt.backLocalTemplate=args.templateFile
    clashOpt.delay=args.delay
    clashOpt.proxy=args.proxy
    clashOpt.nodeOutputToFile=False
    c=clash (clashOpt) 
    c.genYamlToFile()