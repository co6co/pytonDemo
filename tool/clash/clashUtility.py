import requests,base64,yaml,sys,os,math,copy
sys.path.append(os.path.abspath( os.path.join( os.path.dirname(__file__),".."))) #引入log所在绝对目录
import log
import secure
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
    
    def parseYamlNode(nodes:list):
        '''
        解析Yaml文件中的node 节点
        nodes: yaml.get('proxies') 或者 yaml.get('Proxy')
        return :nodes 基本上也是返回 参数，仅作整理过滤
        '''
        nodes_list = []
        for node in nodes:
            node['name'] = node['name'].strip() if node.get('name') else None
            node['server']=node['server'].strip()
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
        return nodes_list
    def parseYaml(yamlContent): # 解析yaml文本
        try:
            yml = yaml.load(yamlContent, Loader=yaml.FullLoader) 
            tmp_list = []
            # clash新字段
            if yml.get('proxies'):tmp_list = yml.get('proxies')
            # clash旧字段
            elif yml.get('Proxy'):tmp_list = yml.get('Proxy')
            else:log.warn('clash节点提取失败,clash节点为空') 
            return clash.parseYamlNode(tmp_list) 
        except:
            raise

    def parseNodeText(text:str| bytes): # 解析 从 base64 解析出来的文本 
        '''
        解析节点
        '''
        nodes_list = text.splitlines() 
        if type(text) == str:
            nodes_list=[itm.encode("utf-8") for itm  in nodes_list]
        clash_node= []
        for node in nodes_list: 
            try:
                if node.startswith(b'vmess://'):
                    decode_proxy = decode_v2ray_node([node]) 
                    clash_node.extend(v2ray_to_clash(decode_proxy))
 
                elif node.startswith(b'ss://'):
                    decode_proxy = decode_ss_node([node])
                    clash_node.extend( ss_to_clash(decode_proxy))
                    
                elif node.startswith(b'ssr://'):
                    decode_proxy = decode_ssr_node([node])
                    clash_node.extend(ssr_to_clash(decode_proxy))

                elif node.startswith(b'trojan://'):
                    decode_proxy = decode_trojan_node([node])
                    clash_node.extend(trojan_to_clash(decode_proxy))
                else:
                    pass 
            except Exception as e:
                log.err(e)
                raise 
        if len(clash_node)>0:return clash_node


    def __getHttpContent(url,proxy:str=None):
        try:
            response = webutility.get(url,proxy=proxy)  
            #print("Encoding:"+response.apparent_encoding,response.encoding)
            response.encoding="utf-8"
            return response.text 
        except Exception as e:
            log.err(f"[-]http请求'{url}'出现异常：{e}")
            pass
    def _genNode(self,nodeContent,nodeContentAddress:str|None): 
        try:
            nodes_list=[]
            yamlData=yaml.full_load(nodeContent) 
            if type (yamlData) == dict: #yaml 格式
                log.succ(f"{type(yamlData)}’yaml dict‘<--{nodeContentAddress}")
                nodes_list=clash.parseYaml(nodeContent)
            elif type (yamlData) == list and type(yamlData[0]) == dict: #yaml 格式中的节点
                log.succ(f"{type(yamlData)} ’yaml list dict‘<--{nodeContentAddress}")
                nodes_list=clash.parseYamlNode(yamlData)
            else: # base64加密 or node list
                log.succ(f"{type(yamlData)} ’TEXT‘<--{nodeContentAddress}")
                rawTxt = base64.b64decode(nodeContent) if secure.base64.isBase64(nodeContent) else nodeContent 
                #log.err(f"{type(rawTxt)},\n{rawTxt}")
               
                nodes_list=clash.parseNodeText(rawTxt)
        except Exception as e:
            log.err('[-]解析节点失败:"{}",{}'.format(e,nodeContentAddress))
            pass
        num=0
        if nodes_list!=None:
            node_names = [node.get('name') for node in nodes_list] 
            num=len(node_names)
            self.proxy_list['proxy_list'].extend(nodes_list)
            self.proxy_list['proxy_names'].extend(node_names)
            log.succ(f'[+]订阅{nodeContentAddress} clash节点数:{num}个')  
            

    def genNodeByUrl(self,subUrl:str):
        '''
        从url中生成节点 
        subUrl      url地址
        '''
    
        log.info(f"订阅：'{subUrl}'...") 
        response=clash.__getHttpContent(subUrl,self.opt.proxy)
        if response==None and opt.proxy!=None:response=clash.__getHttpContent(subUrl)
        if response==None :return 
        self._genNode(response,subUrl)
    
    def genNodeByFile(self,filePath:str):
        '''
        从url中生成节点 
        subUrl      url地址
        ''' 
        log.info(f"订阅：'{filePath}'...") 
        if not os.path.exists(filePath) or not os.path.isfile(filePath):log.warn(f"输入的文件路径'{filePath}'不存在！")
        file=open(filePath,"r",encoding="utf-8") 
        content=file.read()
        file.close()
        self._genNode(content,filePath)

    def genNodeList(self,urlList): #生成 proxy_list 
        '''
        从URL列表中生成节点
        arg: urlList        base64 url|yaml url node list url
        '''
        # 请求订阅地址
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures={executor.submit(self.genNodeByUrl,(url)) for url in urlList}
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
            log.err(f'配置文件{path}加载失败')
            sys.exit(0)

    def getTemplateConfig(url, path,proxy:str=None):
        try:
            raw =   webutility.get(url, timeout=5,proxy=proxy).content.decode('utf-8')
            template_config = yaml.load(raw, Loader=yaml.FullLoader)
        except requests.exceptions.RequestException as e:
            log.warn(f'网络获取规则{url}配置模板失败,加载本地配置文件:\n{e}')
            template_config =clash.load_local_config(path)
        except Exception as e: 
            log.warn(f'网络获取规则{url}配置模板失败,加载本地配置文件,异常信息：\n\t{e}')
            template_config =clash.load_local_config(path)
        log.info('[+]已获取规则配置文件')
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
        if server.replace('.', '').isdigit():ip = server
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
    
 
    def remove_duplicates(nodeList): # 去重
        result = []
        servers = []
        i = 1
        for item in nodeList:
            if 'name' in item:
                if 'server' not in item or 'port' not in item: continue
                domain = item['server']
                port = item['port']
                server=f"{domain}:{port}" 
                if server in servers:
                    log.warn(f"重复节点：{server}")
                    continue  
                servers.append(server)
                #re.match 从字符串开始的地方匹配，
                #re.search 从给定字符串中寻找第一个匹配的子字符串
                #都只能匹配一个
                name=""
                match=re.search('[\u4e00-\u9fa5]+',item['name'])
                if match !=None: name=match.group() 
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
            if model.get('proxies') is None:
                model['proxies'] = data.get('proxy_list')
            else:
                model['proxies'].extend(data.get('proxy_list'))
        except Exception as e:
            log.err(f'Error adding proxies to model: {e}')

        try:
            data['proxy_list'] = [d for d in data['proxy_list'] if 'name' in d]
            names = []
            for item in data['proxy_list']:
                if item['name'] not in names:names.append(item['name'])

            for group in model.get('proxy-groups'):
                if group.get('proxies') is None:
                    #group['proxies'] = data.get('proxy_names')
                    group['proxies'] = names
                else:
                    #group['proxies'].extend(data.get('proxy_names'))
                    group['proxies'].extend(names)
        except Exception as e:
            log.err(f'Error adding proxy names to groups: {e}')
        return model

    # 保存到文件
    def save_to_file(file_name, content):
        with open(file_name, 'wb') as f:
            f.write(content)

    # 保存配置文件
    def save_config(path, data): 
        config = yaml.dump(data, sort_keys=False, default_flow_style=False, encoding='utf-8', allow_unicode=True)
        clash.save_to_file(path, config)
        log.info('[+]成功更新{}个节点'.format(len(data['proxies'])))
    
    def checkNode(node,delay=2000):
        '''
        检测节点
        node : 节点
        delay: 超时 毫秒（超过该时间为失败）
        '''
        if 'server' not in node or 'port' not in node or 'password' in node:
            return False 
        domain = node['server']
        domain=domain .strip()
        node['server']=domain
        port = node['port']
        result=tcp.check_tcp_port({"host":domain,"port":port})
        #log(f"检测节点结果:{result}")
        status=result["status"]
        if status:
            delay=tcp.ping(domain) 
            #log(f"检测网络延迟：{domain}: {delay} ms")
            if delay== None or delay >delay: status= False
        return status
    
    def checkNodes(nodeList,delay:int=1000):
        '''
        检测节点
        '''
        # 去重 
        _nodeList=[]
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures={executor.submit(clash.checkNode,item,delay):item for item in nodeList}
            for future in concurrent.futures.as_completed(futures): 
                item=futures[future] 
                if(future.result()):
                    _nodeList.append(item)
                    log.info(f"[+]'{item['server']}:{item['port']}'.")
                else: log.info(f"[-]'{item['server']}:{item['port']}'.")

        #nameList=[node.get("name") for node in nodeList]     
        return _nodeList
    
    def outputToFile(yamlConfig,nodeList:list,yamlNodeNum:int,outputPath:str): 
        log.info(f'[+]节点数...{len(nodeList)}')
        index=math.floor(len(nodeList) / yamlNodeNum)  
        index+=1 if len(nodeList) % yamlNodeNum > 0 else 0
        i=0
       
        while i<index:
            ii=i*yamlNodeNum
            jj=(i+1)*yamlNodeNum
            data={"proxy_list":[],"proxy_names":[]}
            data["proxy_list"]=nodeList[ii:jj]
            data["proxy_names"]=[item["name"] for item in data["proxy_list"]] 
          
            #输出文件夹
            if i>0: outputPath=os.path.splitext(outputPath)[0]+str(i)+os.path.splitext(outputPath)[1]
            _yamlConfig=copy.deepcopy( yamlConfig )
            final_config =clash.add_proxies_to_model(data, _yamlConfig) 
            clash.save_config(outputPath, final_config)
            i+=1
            
    def genYamlForClash(self,yamlNodeNum:int):
        '''
        desc: 生成yaml 文件
        yamlNodeNum: yaml 节点数
        '''
        self.genNodeList(self.opt.subUrlArray) 
        nodelist=clash.remove_duplicates(self.proxy_list['proxy_list'])
        print("*"*8,self.opt.checkNode)
        if self.opt.checkNode: nodelist=clash.checkNodes(nodelist) 
        log.info("获取导出配置模板...")
        yamlConfig=clash.getTemplateConfig(self.opt.templateUrl,self.opt.backLocalTemplate,self.opt.proxy)
        clash.outputToFile(yamlConfig,nodelist,yamlNodeNum,  self.opt.outputPath)
        
            
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
        self.__delay=1000
        self.__proxy=None
        self.__checkNode=False
    
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

    @property
    def delay(self):
        return self.__delay
    @delay.setter
    def delay(self,value:int):
        self.__delay=value
    
    @property
    def proxy(self):
        return self.__proxy
    @proxy.setter
    def proxy(self,value:str):
        self.__proxy=value

    @property
    def checkNode(self):
        return self.__checkNode
    @checkNode.setter
    def checkNode(self,value:bool):
        self.__checkNode=value

    



if __name__ == '__main__': 
    opt=clashOption(subArray=["https://tt.vg/evIzX"])
    cl =clash (opt)
    cl.genYamlForClash()



