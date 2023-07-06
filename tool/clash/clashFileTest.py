import sys,os,json
import argparse
import htmlparser
from clashUtility import clash,clashOption, log 

if __name__ == '__main__':
    default_output_dir=os.path.join(os.path.abspath("."),"sub")
    default_config_dir=os.path.join(os.path.abspath("."),"file") 

    parser=argparse.ArgumentParser(description="测试clash Yaml文件")
    parser.add_argument("-f","--file",help="clash Yaml Path" ,default="./sub/static-2023-07-06.yaml")
    parser.add_argument("-p","--proxy",help="config proxy address eg. 127.0.0.1:1080")
   
    config=parser.add_argument_group("config")
    config.add_argument("-t","--templateFile",help=f"standby clash yaml templcate File,default:\"{os.path.join(default_config_dir,'clashConfigTemplate.yaml')}\"",default=os.path.join(default_config_dir,"clashConfigTemplate.yaml"))
    
    config=parser.add_argument_group("filter")
    config.add_argument("-d","--delay",  help="node delay within xx ms,default 1000ms ", type=int, default=1000)

    config=parser.add_argument_group("output")
    config.add_argument("-n","--number",  help="node num per yaml,default 150", type=int, default=150)
    config.add_argument("-o",'--outputFolder' , help=f"save yaml file Path,defalut:{default_output_dir}",default=default_output_dir)

    args=parser.parse_args()
    clashOpt=clashOption([])
    clashOpt.outputPath=os.path.join(args.outputFolder,"output-test.yaml")
    clashOpt.backLocalTemplate=args.templateFile
    clashOpt.delay=args.delay
    clashOpt.proxy=args.proxy
    c=clash (clashOpt)
    c.genNodeByFile(args.file)
    nodeList=clash.checkNodes(c.proxy_list['proxy_list'],clashOpt.delay)
    yamlConfig=clash.getTemplateConfig(clashOpt.templateUrl,clashOpt.backLocalTemplate)
    clash.outputToFile(yamlConfig,nodeList,args.number,clashOpt.outputPath)