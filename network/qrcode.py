# coding= utf-8
from pyzbar.pyzbar import decode # pip install pyzbar
from PIL import Image

import cv2 #pip install opencv-python

import optparse

def ewDecode(fileName):
    decocdeQR = decode(Image.open(fileName))
    return decocdeQR[0].data.decode('ascii')

def ewDecode2(qrcode_filename): # 使用 opencv模块(未能识别是来)， 路径不能有中文
    qrcode_image = cv2.imread(qrcode_filename)
    print(qrcode_image)
    qrCodeDetector = cv2.QRCodeDetector()
    data, bbox, straight_qrcode = qrCodeDetector.detectAndDecode(qrcode_image)
    print(straight_qrcode)
    print(bbox)
    return data
 
def main():
     parser=optparse.OptionParser("usage %prog -f <filePath> -t <type 0|1 -0:pyzbar ascii, 1:cv2- >")
     parser.add_option("-f",dest="filePath",type="string",help="文件路径")
     parser.add_option("-t",dest="type",type="int",help="识别方式")
     (opt,args)=parser.parse_args()
    
     if opt.filePath ==None or opt.type not in [0,1]:
         print(parser.usage)
         exit(0)
     elif opt.type ==0:
         print(f'识别到的二维码内容：{ewDecode(opt.filePath)}')
     else:
         print(f'识别到的二维码内容：{ewDecode2(opt.filePath)}')


if __name__ =="__main__":
    main()

