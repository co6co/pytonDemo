import optparse
from clashUtility import clash

if __name__ == '__main__': 
    parser=optparse.OptionParser("usage %prog -d <目录>")
    default_output_dir=f'G:\Tool\SHARE\yaml\cp'
    parser.add_option("-d",dest="dir",type="string",help=f"输入目录默认({default_output_dir})")
    (opt,args)=parser.parse_args()
    if opt.dir == None:
        opt.dir=default_output_dir
        print(parser.usage)
    c=clash ()
    c.genYamlForClash()
    