import optparse,sys,os,json
import argparse
import htmlparser
from clashUtility import clash,clashOption,logger
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

def parse(item):
    try:
        print("调用方法STR：",item["method"]) 
        print("调用方法：", htmlparser.__dict__.get(item["method"]))
        invoke=htmlparser.__dict__.get(item["method"])
        if invoke== None: return  
        url=invoke(item)
        print("关键URL：",url)
        if url!=None and url !="":item["url"]=url
    except Exception as e:
        print(item["remarks"],"出错",e)

def parseSubUrls(jsonFilePath):
    jsonObj=readJsonFile(jsonFilePath)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4)  as executor:
        futures= {executor.submit(parse,item) for item in jsonObj["data"] }
    concurrent.futures.wait(futures,return_when=concurrent.futures.FIRST_COMPLETED)
    writeJsonFile(jsonFilePath,jsonObj)
    return jsonObj 



if __name__ == '__main__': 
    default_output_dir=f'G:\Tool\SHARE\yaml\cp' 
    parser=argparse.ArgumentParser(description="生成clash Yaml文件")
    parser.add_argument("-d",'--folder' , help=f"save yaml file pat,outpu file defalut:{default_output_dir}",default=default_output_dir)
    parser.add_argument("-s",'--subConfigPath' , help=f"sub pach",default=os.path.abspath(os.path.join(default_output_dir,"subUrl.json")))
    parser.add_argument("-n","--number",  help="node num per yaml", type=int, default=150)
    args=parser.parse_args()
    
    #urls=readFile(args.subConfigPath)
    print("解析生成url...")
    jsonData=parseSubUrls(args.subConfigPath)
    urls=[item["url"] for item in jsonData["data"]]
     
    clashOpt=clashOption(urls)

    clashOpt.outputPath=os.path.join(args.folder,"output.yaml")
    clashOpt.backLocalTemplate=os.path.join(default_output_dir,"clashConfigTemplate.yaml")
    c=clash (clashOpt)
    c.genYamlForClash(args.number) 
    