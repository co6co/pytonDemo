import os,sys
from commands import Protection,Command
import optparse


if __name__ == "__main__":
    parser=optparse.OptionParser("usage %prog -s <serviceName>")
    parser.add_option("-s",dest="serviceName",type="string",help="Service Name")
    (opt,args)=parser.parse_args()
    if opt.serviceName ==None:
        print(parser.usage)
        exit(0)
    else:            
        checkCommand=Command(f"sc query {opt.serviceName}",resultContain="STATE              : 4  RUNNING")
        successCommand=Command(f"sc query {opt.serviceName}",resultContain="STATE              : 4  RUNNING")
        faileCommand=Command(f"sc start {opt.serviceName}",resultContain="STATE              : 4  RUNNING")
        p=Protection(checkCommand,failCommand=faileCommand,successCommand=successCommand)
        p.check()



             
