
import sys
sys.path.append("../")
from log import log
import json,base64,re
import urllib.parse

def safe_decode(s):
    #print("saft_decode:",s)
    num = len(s) % 4
    if num:
        s += '=' * (4 - num)
    #print(f"s:{s},num:{num}")
    return base64.urlsafe_b64decode(s)

# 解析vmess节点
def decode_v2ray_node(nodes):
    proxy_list = []
    for node in nodes:
        decode_proxy = node.decode('utf-8')[8:]
        if not decode_proxy or decode_proxy.isspace():
            log('vmess节点信息为空，跳过该节点')
            continue
        proxy_str = base64.b64decode(decode_proxy).decode('utf-8')
        proxy_dict = json.loads(proxy_str)
        proxy_list.append(proxy_dict)
    #print(proxy_list)
    return proxy_list

# 解析ss节点
def decode_ss_node(nodes):
    proxy_list = []
    for node in nodes:
        decode_proxy = node.decode('utf-8')[5:]
        if not decode_proxy or decode_proxy.isspace():
            log('ss节点信息为空，跳过该节点')
            continue
        info = dict()
        param = decode_proxy
        if param.find('#') > -1:
            remark = urllib.parse.unquote(param[param.find('#') + 1:])
            info['name'] = remark
            param = param[:param.find('#')]
        if param.find('/?') > -1:
            plugin = urllib.parse.unquote(param[param.find('/?') + 2:])
            param = param[:param.find('/?')]
            for p in plugin.split(';'):
                key_value = p.split('=')
                info[key_value[0]] = key_value[1]
        if param.find('@') > -1:
            matcher = re.match(r'(.*?)@(.*):(.*)', param)
            if matcher:
                param = matcher.group(1)
                info['server'] = matcher.group(2)
                info['port'] = matcher.group(3)
            else:
                continue
            matcher = re.match(
                r'(.*?):(.*)', safe_decode(param).decode('utf-8'))
            if matcher:
                info['method'] = matcher.group(1)
                info['password'] = matcher.group(2)
            else:
                continue
        else:
            matcher = re.match(r'(.*?):(.*)@(.*):(.*)',
                               safe_decode(param).decode('utf-8'))
            if matcher:
                info['method'] = matcher.group(1)
                info['password'] = matcher.group(2)
                info['server'] = matcher.group(3)
                info['port'] = matcher.group(4)
            else:
                continue
        proxy_list.append(info)
    #print(proxy_list)
    return proxy_list


# 解析ssr节点
def decode_ssr_node(nodes):
    proxy_list = []
    for node in nodes:
        decode_proxy = node.decode('utf-8')[6:]
        if not decode_proxy or decode_proxy.isspace():
            log('ssr节点信息为空，跳过该节点')
            continue
        proxy_str = safe_decode(decode_proxy).decode('utf-8')
        parts = proxy_str.split(':')
        if len(parts) != 6:
            print('该ssr节点解析失败，链接:{}'.format(node))
            continue
        info = {
            'server': parts[0],
            'port': parts[1],
            'protocol': parts[2],
            'method': parts[3],
            'obfs': parts[4]
        }
        password_params = parts[5].split('/?')
        info['password'] = safe_decode(password_params[0]).decode('utf-8')
        params = password_params[1].split('&')
        for p in params:
            key_value = p.split('=')
            info[key_value[0]] = safe_decode(key_value[1]).decode('utf-8')
        proxy_list.append(info)
    return proxy_list

#解析Trojan节点
def decode_trojan_node(nodes):
    proxy_list = []
    info = {}
    for node in nodes:
        info = dict()
        try:
            node = urllib.parse.unquote(node)
            parsed_url = node.replace('trojan://', '')
            part_list = re.split('#', parsed_url, maxsplit=1)
            info.setdefault('name', part_list[1])
            server_part = part_list[0].replace('trojan://', '')
            server_part_list = re.split(':|@|\?|&', server_part)
            info.setdefault('server', server_part_list[1])
            info.setdefault('port', int(server_part_list[2]))
            info.setdefault('type', 'trojan')
            info.setdefault('password', server_part_list[0])
            server_part_list = server_part_list[3:]
            for config in server_part_list:
                if 'sni=' in config:
                    info.setdefault('sni', config[4:])
                elif 'allowInsecure=' in config or 'tls=' in config:
                    if config[-1] == 0:
                        info.setdefault('tls', False)
                elif 'type=' in config:
                    if config[5:] != 'tcp':
                        info.setdefault('network', config[5:])
                elif 'path=' in config:
                    info.setdefault('ws-path', config[5:])
                elif 'security=' in config:
                    if config[9:] != 'tls':
                        info.setdefault('tls', False)
            info.setdefault('skip-cert-verify', True)
            proxy_list.append(info)
        except Exception as e:
            print(f"解析trojan出错{e}")
    #print(proxy_list)
    return proxy_list
