

import sys,os

from  co6co.utils.log import log,warn

# Vmess转换成Clash节点
def v2ray_to_clash(v2rayArr):
    proxies =[]
    num = 0
    for item in v2rayArr:
        num += 1
        if item.get('ps') is None and item.get('add') is None and item.get('port') is None \
                and item.get('id') is None and item.get('aid') is None:
            continue
        obj = {
            'name': item.get('ps').strip() if item.get('ps') else None,
            #'name': f"Auto_proxy{num}",
            'type': 'vmess',
            'server': item.get('add').strip(),
            'port': int(item.get('port')),
            'uuid': item.get('id'),
            'alterId': int(item.get('aid')),
            'cipher': 'auto',
            'udp': True,
            # 'network': item['net'] if item['net'] and item['net'] != 'tcp' else None,
            'network': item.get('net'),
            'tls': True if item.get('tls') == 'tls' else None,
            'ws-path': item.get('path'),
            'ws-headers': {'Host': item.get('host')} if item.get('host') else None
        }
        
        for key in list(obj.keys()):
            if obj.get(key) is None:
                del obj[key]
        #'''
        if obj.get('alterId') is not None:
            try:
                proxies.append(obj) 
            except Exception as e:
                log(f'V2ray出错{e}')
        #''' 
    return proxies

# ss转换成Clash节点
def ss_to_clash(ssArr): 
    proxies =[]
    for item in ssArr:
        obj = {
            'name': item.get('name').strip() if item.get('name') else None,
            'type': 'ss',
            'server': item.get('server').strip(),
            'port': int(item.get('port')),
            'cipher': item.get('method'),
            'password': item.get('password'),
            'plugin': 'obfs' if item.get('plugin') and item.get('plugin').startswith('obfs') else None,
            'plugin-opts': {} if item.get('plugin') else None
        }
        if item.get('obfs'):
            obj['plugin-opts']['mode'] = item.get('obfs')
        if item.get('obfs-host'):
            obj['plugin-opts']['host'] = item.get('obfs-host')
        for key in list(obj.keys()):
            if obj.get(key) is None:
                del obj[key]
        try:
            proxies.append(obj)
        except Exception as e:
            log(f'出错{e}')
            pass
    #print(proxies)
    return proxies

# ssr转换成Clash节点
def ssr_to_clash(ssrArr):
    log('ssr节点转换中...')
    cipherArr=("aes-128-gcm","aes-192-gcm","aes-256-gcm","aes-128-cfb","aes-192-cfb","aes-256-cfb","aes-128-ctr","aes-192-ctr","aes-256-ctr",
               "rc4-md5","rc4",
               "chacha20","chacha20-ietf","xchacha20","chacha20-ietf-poly1305","plain" ,"http_simple","auth_sha1_v4","auth_aes128_md5",
               "auth_aes128_sha1","auth_chain_a","auth_chain_b")
    proxies = []
    for item in ssrArr:
        obj = {
            'name': item.get('remarks').strip() if item.get('remarks') else None,
            'type': 'ssr',
            'server': item.get('server').strip(),
            'port': int(item.get('port')),
            'cipher': item.get('method'),
            'password': item.get('password'),
            'obfs': item.get('obfs'),
            'protocol': item.get('protocol'),
            'obfs-param': item.get('obfsparam'),
            'protocol-param': item.get('protoparam'),
            'udp': True
        }
        try:
            for key in list(obj.keys()):
                if obj.get(key) is None:
                    del obj[key]
            if obj.get('name'):
                #print(obj['cipher'])
                if not obj['name'].startswith('剩余流量') and not obj['name'].startswith('过期时间'):
                    if obj['cipher'] in cipherArr: proxies.append(obj) 
                    else: log(f"不支持的ssr 算法{ obj['cipher']}")
        except Exception as e:
            log(f'ssr 转换出错{e}')  
    log('可用ssr节点{}个'.format(len(proxies)))
    return proxies

#将Trojan节点转clash
def trojan_to_clash(trojanArr): 
    proxies =[]
    for item in trojanArr:
        try:
           proxies.append(item)
        except Exception as e:
            log(f'出错{e}')
            pass 
    #print(proxies)
    return proxies