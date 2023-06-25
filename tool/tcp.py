# -*- coding: utf-8 -*-
import socket

'''
opt:{host:domainName|ip,port:PortNumber}
'''
def check_tcp_port(opt:dict, timeout=2):
    try:
       #socket.AF_INET 服务器之间网络通信
       #socket.SOCK_STREAM  流式socket , 当使用TCP时选择此参数
        cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = (str(opt["host"]), int(opt["port"]))
        cs.settimeout(timeout)
        #s.connect_ex(adddress)功能与connect(address)相同，但是成功返回0，失败返回error的值。
        status = cs.connect_ex(address)
    except Exception as e:
        return {"status": False, "message": str(e), "info": "tcp check"}
    else:
        if status != 0:
            return {"status": False, "message": "Connection %s:%s failed" % (opt["host"], opt["port"]),
                    "info": "tcp check"}
        else:
            return {"status": True, "message": "OK", "info": "tcp check"}

if __name__ == "__main__":
    print (check_tcp_port({"host":"www.baidu.com","port":80}))
 