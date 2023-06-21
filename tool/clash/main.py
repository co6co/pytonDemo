import optparse,sys,os
from clashUtility import clash,clashOption,logger
sys.path.append(os.path.dirname(os.path.abspath(sys.argv[0])+"../tool"))

if __name__ == '__main__': 
    parser=optparse.OptionParser("usage %prog -d <目录> -s <config文件——订阅URL>")
    default_output_dir=f'G:\Tool\SHARE\yaml\cp'
    parser.add_option("-d",dest="folder",type="string",help=f"输入目录默认({default_output_dir})")
    parser.add_option("-s",dest="configPath",type="string",help=f"输入目录默认({default_output_dir})")
    (opt,args)=parser.parse_args()
    if opt.folder == None:
        opt.folder=default_output_dir
        print(parser.usage)
    if opt.configPath == None:
        opt.configPath=os.path.abspath(os.path.join(default_output_dir,"subUrl.txt"))
        print("默认的订阅配置：",opt.configPath)
    if(not os.path.exists(opt.configPath)):
         print("配置文件不存在！！",opt.configPath)
         exit(0)

    file=open(opt.configPath,"r",encoding='utf-8')
    urls=file.read().splitlines()# readlines() 会存在\n
    clashOpt=clashOption(urls)
    clashOpt.outputPath=os.path.join(opt.folder,"output.yaml")
    clashOpt.backLocalTemplate=os.path.join(default_output_dir,"clashConfigTemplate.yaml")
    c=clash (clashOpt)
    c.genYamlForClash()
    