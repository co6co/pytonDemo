import optparse,sys,os
import argparse
from clashUtility import clash,clashOption,logger
sys.path.append(os.path.dirname(os.path.abspath(sys.argv[0])+"../tool"))

if __name__ == '__main__': 
    default_output_dir=f'G:\Tool\SHARE\yaml\cp' 
    parser=argparse.ArgumentParser(description="生成clash Yaml文件")
    parser.add_argument("-d",'--folder' , help=f"save yaml file pat,outpu file defalut:{default_output_dir}",default=default_output_dir)
    parser.add_argument("-s",'--subConfigPath' , help=f"sub pach",default=os.path.abspath(os.path.join(default_output_dir,"subUrl.txt")))
    parser.add_argument("-n","--number",  help="node num per yaml", type=int, default=150)
    args=parser.parse_args()
    args.folder
    
    file=open(args.subConfigPath,"r",encoding='utf-8')
    urls=file.read().splitlines()# readlines() 会存在\n
    clashOpt=clashOption(urls)
    clashOpt.outputPath=os.path.join(args.folder,"output.yaml")
    clashOpt.backLocalTemplate=os.path.join(default_output_dir,"clashConfigTemplate.yaml")
    c=clash (clashOpt)
    c.genYamlForClash(args.number)
    