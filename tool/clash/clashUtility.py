import requests,base64,yaml,sys,os,math
sys.path.append(os.path.abspath( os.path.join( os.path.dirname(__file__),".."))) #引入log所在绝对目录
from log import log,logger
import tcp
import webutility
from convert2clash import *
from parserNode import *
import geoip2.database
import socket,  concurrent.futures




class clash:
    proxy_list = {
        'proxy_list': [],
        'proxy_names': []
    } 

    #命名数字
    vmess = [] 
  
    def __init__(self,clashOption) -> None:
        self.opt=clashOption
        pass
    def parseYaml(self,content): # 解析yaml文本
        try:
            yml = yaml.load(content, Loader=yaml.FullLoader,)
            nodes_list = []
            tmp_list = []
            # clash新字段
            if yml.get('proxies'):
                tmp_list = yml.get('proxies')
            # clash旧字段
            elif yml.get('Proxy'):
                tmp_list = yml.get('Proxy')
            else:
                log('clash节点提取失败,clash节点为空') 
            
            for node in tmp_list:
                node['name'] = node['name'].strip() if node.get('name') else None
                
                # 对clashR的支持
                if node.get('protocolparam'):
                    node['protocol-param'] = node['protocolparam']
                    del node['protocolparam']
                if node.get('obfsparam'):
                    node['obfs-param'] = node['obfsparam']
                    del node['obfsparam']
                node['udp'] = True
                node['port'] = int(node['port']) 
                 
                if node.get('name')==None: continue
                nodes_list.append(node)

            node_names = [node.get('name') for node in nodes_list]
            log('可用clash节点{}个'.format(len(node_names)))
            self.proxy_list['proxy_list'].extend(nodes_list)
            self.proxy_list['proxy_names'].extend(node_names)
        except Exception as e:
            print ("内容不正确",e)

    def parseNodeText(self,text): # 解析 从 base64 解析出来的文本
        nodes_list = text.splitlines()  
        nodes_list.extend(self.vmess)
        clash_node = []
        for node in nodes_list: 
            try:
                if node.startswith(b'vmess://'):
                    decode_proxy = decode_v2ray_node([node])
                    clash_node = v2ray_to_clash(decode_proxy)
 
                elif node.startswith(b'ss://'):
                    decode_proxy = decode_ss_node([node])
                    clash_node = ss_to_clash(decode_proxy)
                    
                elif node.startswith(b'ssr://'):
                    decode_proxy = decode_ssr_node([node])
                    clash_node = ssr_to_clash(decode_proxy)

                elif node.startswith(b'trojan://'):
                    decode_proxy = decode_trojan_node([node])
                    clash_node = trojan_to_clash(decode_proxy)
                    
                else:
                    pass
                
                log('可用clash节点{}个'.format(len(clash_node['proxy_list'])))
                self.proxy_list['proxy_list'].extend(clash_node['proxy_list']) 
                self.proxy_list['proxy_names'].extend(clash_node['proxy_names'])
            except Exception as e:
                print(f'出错{e}')

    def _genNode(self,subUrl):
        if not subUrl.lower().startswith("http"):return
        log(f"订阅：'{subUrl}'...")
        try:
            response = webutility.get(subUrl) 
            print("Encoding:"+response.apparent_encoding)
            response.encoding="utf-8"
            response=response.text
        except Exception as e:
            log(f"http请求'{subUrl}'出现异常：{e}")
            return
        try:
            raw = base64.b64decode(response)
            self.parseNodeText(raw)
        except Exception as e:
            log('base64解码失败:"{}",应当为clash节点'.format(e))
            log('clash节点提取中...')
            self.parseYaml(response) 
    def genNodeList(self,urlList): #生成 proxy_list 
        # 请求订阅地址
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures={executor.submit(self._genNode,(url)) for url in urlList}
        concurrent.futures.wait(futures,return_when=concurrent.futures.FIRST_COMPLETED)
        #for future in concurrent.futures.as_completed(futures):
        #    future.done()
            

    # 获取本地规则策略的配置文件
    def load_local_config(path):
        try:
            f = open(path, 'r', encoding="utf-8")
            local_config = yaml.load(f.read(), Loader=yaml.FullLoader)
            f.close()
            return local_config
        except FileNotFoundError:
            log(f'配置文件{path}加载失败')
            sys.exit(0)

    def getTemplateConfig(self,url, path):
        try:
            raw =   webutility.get(url, timeout=5).content.decode('utf-8')
            template_config = yaml.load(raw, Loader=yaml.FullLoader)
            a=1/0
        except requests.exceptions.RequestException:
            log(f'网络获取规则{url}配置模板失败,加载本地配置文件')
            template_config =clash.load_local_config(path)
        except Exception as e: 
            log(f'网络获取规则{url}配置模板失败,加载本地配置文件,异常信息：\n\t{e}')
            template_config =clash.load_local_config(path)
        log('已获取规则配置文件')
        return template_config
    
    def find_country(server):
        emoji = {
            'AD': '🇦🇩', 'AE': '🇦🇪', 'AF': '🇦🇫', 'AG': '🇦🇬',
            'AI': '🇦🇮', 'AL': '🇦🇱', 'AM': '🇦🇲', 'AO': '🇦🇴',
            'AQ': '🇦🇶', 'AR': '🇦🇷', 'AS': '🇦🇸', 'AT': '🇦🇹',
            'AU': '🇦🇺', 'AW': '🇦🇼', 'AX': '🇦🇽', 'AZ': '🇦🇿',
            'BA': '🇧🇦', 'BB': '🇧🇧', 'BD': '🇧🇩', 'BE': '🇧🇪',
            'BF': '🇧🇫', 'BG': '🇧🇬', 'BH': '🇧🇭', 'BI': '🇧🇮',
            'BJ': '🇧🇯', 'BL': '🇧🇱', 'BM': '🇧🇲', 'BN': '🇧🇳',
            'BO': '🇧🇴', 'BQ': '🇧🇶', 'BR': '🇧🇷', 'BS': '🇧🇸',
            'BT': '🇧🇹', 'BV': '🇧🇻', 'BW': '🇧🇼', 'BY': '🇧🇾',
            'BZ': '🇧🇿', 'CA': '🇨🇦', 'CC': '🇨🇨', 'CD': '🇨🇩',
            'CF': '🇨🇫', 'CG': '🇨🇬', 'CH': '🇨🇭', 'CI': '🇨🇮',
            'CK': '🇨🇰', 'CL': '🇨🇱', 'CM': '🇨🇲', 'CN': '🇨🇳',
            'CO': '🇨🇴', 'CR': '🇨🇷', 'CU': '🇨🇺', 'CV': '🇨🇻',
            'CW': '🇨🇼', 'CX': '🇨🇽', 'CY': '🇨🇾', 'CZ': '🇨🇿',
            'DE': '🇩🇪', 'DJ': '🇩🇯', 'DK': '🇩🇰', 'DM': '🇩🇲',
            'DO': '🇩🇴', 'DZ': '🇩🇿', 'EC': '🇪🇨', 'EE': '🇪🇪',
            'EG': '🇪🇬', 'EH': '🇪🇭', 'ER': '🇪🇷', 'ES': '🇪🇸',
            'ET': '🇪🇹', 'EU': '🇪🇺', 'FI': '🇫🇮', 'FJ': '🇫🇯',
            'FK': '🇫🇰', 'FM': '🇫🇲', 'FO': '🇫🇴', 'FR': '🇫🇷',
            'GA': '🇬🇦', 'GB': '🇬🇧', 'GD': '🇬🇩', 'GE': '🇬🇪',
            'GF': '🇬🇫', 'GG': '🇬🇬', 'GH': '🇬🇭', 'GI': '🇬🇮',
            'GL': '🇬🇱', 'GM': '🇬🇲', 'GN': '🇬🇳', 'GP': '🇬🇵',
            'GQ': '🇬🇶', 'GR': '🇬🇷', 'GS': '🇬🇸', 'GT': '🇬🇹',
            'GU': '🇬🇺', 'GW': '🇬🇼', 'GY': '🇬🇾', 'HK': '🇭🇰',
            'HM': '🇭🇲', 'HN': '🇭🇳', 'HR': '🇭🇷', 'HT': '🇭🇹',
            'HU': '🇭🇺', 'ID': '🇮🇩', 'IE': '🇮🇪', 'IL': '🇮🇱',
            'IM': '🇮🇲', 'IN': '🇮🇳', 'IO': '🇮🇴', 'IQ': '🇮🇶',
            'IR': '🇮🇷', 'IS': '🇮🇸', 'IT': '🇮🇹', 'JE': '🇯🇪',
            'JM': '🇯🇲', 'JO': '🇯🇴', 'JP': '🇯🇵', 'KE': '🇰🇪',
            'KG': '🇰🇬', 'KH': '🇰🇭', 'KI': '🇰🇮', 'KM': '🇰🇲',
            'KN': '🇰🇳', 'KP': '🇰🇵', 'KR': '🇰🇷', 'KW': '🇰🇼',
            'KY': '🇰🇾', 'KZ': '🇰🇿', 'LA': '🇱🇦', 'LB': '🇱🇧',
            'LC': '🇱🇨', 'LI': '🇱🇮', 'LK': '🇱🇰', 'LR': '🇱🇷',
            'LS': '🇱🇸', 'LT': '🇱🇹', 'LU': '🇱🇺', 'LV': '🇱🇻',
            'LY': '🇱🇾', 'MA': '🇲🇦', 'MC': '🇲🇨', 'MD': '🇲🇩',
            'ME': '🇲🇪', 'MF': '🇲🇫', 'MG': '🇲🇬', 'MH': '🇲🇭',
            'MK': '🇲🇰', 'ML': '🇲🇱', 'MM': '🇲🇲', 'MN': '🇲🇳',
            'MO': '🇲🇴', 'MP': '🇲🇵', 'MQ': '🇲🇶', 'MR': '🇲🇷',
            'MS': '🇲🇸', 'MT': '🇲🇹', 'MU': '🇲🇺', 'MV': '🇲🇻',
            'MW': '🇲🇼', 'MX': '🇲🇽', 'MY': '🇲🇾', 'MZ': '🇲🇿',
            'NA': '🇳🇦', 'NC': '🇳🇨', 'NE': '🇳🇪', 'NF': '🇳🇫',
            'NG': '🇳🇬', 'NI': '🇳🇮', 'NL': '🇳🇱', 'NO': '🇳🇴',
            'NP': '🇳🇵', 'NR': '🇳🇷', 'NU': '🇳🇺', 'NZ': '🇳🇿',
            'OM': '🇴🇲', 'PA': '🇵🇦', 'PE': '🇵🇪', 'PF': '🇵🇫',
            'PG': '🇵🇬', 'PH': '🇵🇭', 'PK': '🇵🇰', 'PL': '🇵🇱',
            'PM': '🇵🇲', 'PN': '🇵🇳', 'PR': '🇵🇷', 'PS': '🇵🇸',
            'PT': '🇵🇹', 'PW': '🇵🇼', 'PY': '🇵🇾', 'QA': '🇶🇦',
            'RE': '🇷🇪', 'RO': '🇷🇴', 'RS': '🇷🇸', 'RU': '🇷🇺',
            'RW': '🇷🇼', 'SA': '🇸🇦', 'SB': '🇸🇧', 'SC': '🇸🇨',
            'SD': '🇸🇩', 'SE': '🇸🇪', 'SG': '🇸🇬', 'SH': '🇸🇭',
            'SI': '🇸🇮', 'SJ': '🇸🇯', 'SK': '🇸🇰', 'SL': '🇸🇱',
            'SM': '🇸🇲', 'SN': '🇸🇳', 'SO': '🇸🇴', 'SR': '🇸🇷',
            'SS': '🇸🇸', 'ST': '🇸🇹', 'SV': '🇸🇻', 'SX': '🇸🇽',
            'SY': '🇸🇾', 'SZ': '🇸🇿', 'TC': '🇹🇨', 'TD': '🇹🇩',
            'TF': '🇹🇫', 'TG': '🇹🇬', 'TH': '🇹🇭', 'TJ': '🇹🇯',
            'TK': '🇹🇰', 'TL': '🇹🇱', 'TM': '🇹🇲', 'TN': '🇹🇳',
            'TO': '🇹🇴', 'TR': '🇹🇷', 'TT': '🇹🇹', 'TV': '🇹🇻',
            'TW': '🇹🇼', 'TZ': '🇹🇿', 'UA': '🇺🇦', 'UG': '🇺🇬',
            'UM': '🇺🇲', 'US': '🇺🇸', 'UY': '🇺🇾', 'UZ': '🇺🇿',
            'VA': '🇻🇦', 'VC': '🇻🇨', 'VE': '🇻🇪', 'VG': '🇻🇬',
            'VI': '🇻🇮', 'VN': '🇻🇳', 'VU': '🇻🇺', 'WF': '🇼🇫',
            'WS': '🇼🇸', 'XK': '🇽🇰', 'YE': '🇾🇪', 'YT': '🇾🇹',
            'ZA': '🇿🇦', 'ZM': '🇿🇲', 'ZW': '🇿🇼',
            'RELAY': '🏁',
            'NOWHERE': '🇦🇶',
        }
        if server.replace('.', '').isdigit():
            ip = server
        else:
            try:
                # https://cloud.tencent.com/developer/article/1569841
                ip = socket.gethostbyname(server)
            except Exception:
                ip = server
        with geoip2.database.Reader('./file/ip/Country.mmdb') as ip_reader:
            try:
                response = ip_reader.country(ip)
                country_code = response.country.iso_code
            except Exception:
                ip = '0.0.0.0'
                country_code = 'NOWHERE'

        if country_code == 'CLOUDFLARE':
            country_code = 'RELAY'
        elif country_code == 'PRIVATE':
            country_code = 'RELAY'
        if country_code in emoji:
            name_emoji = emoji[country_code]
        else:
            name_emoji = emoji['NOWHERE']
        return '[' + name_emoji + ']'
    
 
    def remove_duplicates(lst): # 去重
        result = []
        namesl = []
        servers = []
        i = 1
        for item in lst:
            if 'name' in item:
                if 'server' not in item or 'port' not in item:
                    continue
                domain = item['server']
                port = item['port']
                server=f"{domain}:{port}" 
                if server in servers:
                    continue  
                servers.append(server)
                #re.match 从字符串开始的地方匹配，
                #re.search 从给定字符串中寻找第一个匹配的子字符串
                #都只能匹配一个
                name=""
                match=re.search('[\u4e00-\u9fa5]+',item['name'])
                if match !=None:
                    name=match.group()

                '''
                名称转换为指定格式
                ''' 
                '''
                pattern = '[^\u4e00-\u9fa5\d]+'
                item['name'] = re.sub(pattern, '', item['name'] ) 
                item['name'] = re.sub(r'\d', '', item['name'])
                location = item['name'][:3] 
                # Check for duplicate names and append an index if needed
                original_name = location
                index = 1
                while item['name'] in namesl:
                    item['name'] = original_name + '_' + str(index)
                    index += 1

                namesl.append(item['name'])
                item['name'] = location + '_' + str(i)
                '''

                item['name']=clash.find_country(domain)+ name+'_' + str(i)
                result.append(item)
            i += 1
        return result
    # 将代理添加到配置文件
    def add_proxies_to_model(data, model):
        if data is None or model is None:
            raise ValueError('Invalid input: data and model cannot be None')
        if 'proxy_list' not in data or 'proxy_names' not in data:
            raise ValueError('Invalid input: data should contain "proxy_list" and "proxy_names" keys')
        
        try:
            data['proxy_list'] = clash.remove_duplicates(data['proxy_list'])
            if model.get('proxies') is None:
                model['proxies'] = data.get('proxy_list')
            else:
                model['proxies'].extend(data.get('proxy_list'))
        except Exception as e:
            log(f'Error adding proxies to model: {e}')

        try:
            data['proxy_list'] = [d for d in data['proxy_list'] if 'name' in d]
            names = []
            for item in data['proxy_list']:
                if item['name'] not in names:
                    names.append(item['name'])
            for group in model.get('proxy-groups'):
                if group.get('proxies') is None:
                    #group['proxies'] = data.get('proxy_names')
                    group['proxies'] = names
                else:
                    #group['proxies'].extend(data.get('proxy_names'))
                    group['proxies'].extend(names)
        except Exception as e:
            log(f'Error adding proxy names to groups: {e}')
        return model

    # 保存到文件
    def save_to_file(file_name, content):
        with open(file_name, 'wb') as f:
            f.write(content)

    # 保存配置文件
    def save_config(path, data): 
        config = yaml.dump(data, sort_keys=False, default_flow_style=False, encoding='utf-8', allow_unicode=True)
        clash.save_to_file(path, config)
        log('成功更新{}个节点'.format(len(data['proxies'])))
    
    def checkNode(node):
        if 'server' not in node or 'port' not in node or 'password' in node:
            return False
                        
        domain = node['server']
        port = node['port']
        result=tcp.check_tcp_port({"host":domain,"port":port})
        #log(f"检测节点结果:{result}")
        status=result["status"]
        if status:
            delay=tcp.ping(domain) 
            #log(f"检测网络延迟：{domain}: {delay} ms")
            if delay== None or delay >2000: status= False
        return status
    
    def check_nodes(self):
        nodeList=[]
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures={executor.submit(clash.checkNode,item):item for item in self.proxy_list['proxy_list']}
            log("*"*10)
            for future in concurrent.futures.as_completed(futures): 
                item=futures[future] 
                if(future.result()):nodeList.append(item)
                else: log(f"检测失败的节点：{item['server']}:{item['port']}.")
             
        self.proxy_list['proxy_list']=nodeList
        self.proxy_list['proxy_names']=[node.get("name") for node in nodeList]
  
    def genYamlForClash(self,yamlNodeNum:int):
        config_path = self.opt.backLocalTemplate
        clashOpt=self.opt
        log("获取导出配置模板...")
        yamlConfig=self.getTemplateConfig(clashOpt.templateUrl,config_path)
        log(f"获取导出节点...") 
        self.genNodeList(self.opt.subUrlArray) 
        self.check_nodes() 
        log(f'通过模板导出配置文件...{len(self.proxy_list.get("proxy_list"))}')
        
        index=math.floor(len(self.proxy_list.get("proxy_list")) / yamlNodeNum)  
        index+=1 if len(self.proxy_list.get("proxy_list")) % yamlNodeNum >0 else 0
        i=0
               

        while i<index:
            ii=i*yamlNodeNum
            jj=(i+1)*yamlNodeNum
            data={"proxy_list":[],"proxy_names":[]}
            data["proxy_list"]=self.proxy_list['proxy_list'][ii:jj]
            data["proxy_names"]=self.proxy_list['proxy_names'][ii:jj]

            
            outputPath=clashOpt.outputPath
            if i>0: outputPath=os.path.splitext(outputPath)[0]+str(i)+os.path.splitext(outputPath)[1]
            final_config =clash.add_proxies_to_model(data, yamlConfig) 
            log(f'clash文件导出至{outputPath}.')
            clash.save_config(outputPath, final_config)
            i+=1
        

class clashOption():
    def __init__(self,subArray=list):
    
        #模板 __xxxx 私有属性不能被继承
        self.__templateUrl="https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/config.yaml" 
        self.__templateUrl="https://raw.githubusercontent.com/co6co/pytonDemo/master/file/clashConfigTemplate.yaml"
        # 备用本地模板
        self.__backLocalTemplate="./default_config.yaml"
        self.subUrlArray=subArray
        #输出
        self.__outputPath='./file/output.yaml'
    
    @property  #像访问属性一样访问方法
    def templateUrl(self): 
        return self.__templateUrl
    @templateUrl.setter
    def templateUrl(self,value:str):
        self.__templateUrl=value

    @property  #备用本地模板
    def backLocalTemplate(self): 
        return self.__backLocalTemplate
    @backLocalTemplate.setter
    def backLocalTemplate(self,value:str):
        self.__backLocalTemplate=value
    
    @property
    def outputPath(self):
        return self.__outputPath
    @outputPath.setter
    def outputPath(self,value:str):
        self.__outputPath=value



if __name__ == '__main__': 
    opt=clashOption(subArray=["https://tt.vg/evIzX"])
    cl =clash (opt)
    cl.genYamlForClash()



