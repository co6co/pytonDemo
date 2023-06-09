import PyPDF2
from PyPDF2 import PdfFileReader
import optparse 
##
## 获取 PDF 的 Meta 信息
##
def printMeta(fileName):  
    reader= PyPDF2.PdfReader(open(fileName,'rb')) 
    metadata=reader.metadata
    print('[*] PDF MetaData For: ' + str(fileName))
    for item in metadata:
        print('[+] ' + item + ':' + metadata[item])

def main():
 parser = optparse.OptionParser('usage %prog -F <PDF file name>')
 parser.add_option('-F', dest='fileName', type='string',help='specify PDF file name')
 (options, args) = parser.parse_args()
 fileName = options.fileName
 if fileName == None:
    print(parser.usage)
    exit(0)
 else:
    printMeta(fileName)
    
if __name__ == '__main__':
    main()