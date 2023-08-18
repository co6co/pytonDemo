import requests,yaml,sys,os,math,copy,re
from co6co_clash import nodes
sys.path.append(os.path.abspath( os.path.join( os.path.dirname(__file__),".."))) #引入上级目录
import tcp
import co6co.utils.http as webutility 
import geoip2.database
import socket,  concurrent.futures
import uuid
import co6co.utils.log as log

class resourceType:
    '''
    枚举： 资源类型
    '''
    http=0,
    file=1
class nodeResource:
    '''
    节点资源
    '''
    def __init__(self,id:int,reType:resourceType,add:str ) -> None:
        self.__id=id
        self.__type=reType
        self.__address=add 
    @property
    def id(self):
        return self.__id
    @id.setter
    def id(self,value:int):
        self.__id=value
    @property
    def resourceType(self):
        return self.__type
    @resourceType.setter
    def resourceType(self,value:resourceType):
        self.__type=value
    @property
    def address(self):
        return self.__address
    @address.setter
    def address(self,value:resourceType):
        self.__address=value

class clashOption():
    def __init__(self,noderesources=list ):
        #模板 __xxxx 私有属性不能被继承
        self.__templateUrl="https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/config.yaml" 
        self.__templateUrl="https://raw.githubusercontent.com/co6co/pytonDemo/master/file/clashConfigTemplate.yaml"
        # 备用本地模板
        self.__backLocalTemplate="./default_config.yaml"
        self.noderesources=noderesources
        #输出
        self.__outputPath='./file'
        self.__delay=1000
        self.__proxy=None
        self.__checkNode=False
        self.__nodeOutputToFile=False
    
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
        '''
        输出文件夹
        '''
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
    
    @property
    def nodeOutputToFile(self):
        return self.__nodeOutputToFile
    @nodeOutputToFile.setter
    def nodeOutputToFile(self,value:bool):
        self.__nodeOutputToFile=value
    
 

class clash:
    _outputYamlFileName="output.yaml"
    #命名数字
    vmess = [] 
  
    def __init__(self,opt:clashOption) -> None:
        self.opt=opt
        pass   
    def __saveFile(self,resource:nodeResource,node_list):
        try:
            
            if len(node_list) ==0 or node_list ==None:
                log.warn (f"[-]节点数:0,不保存文件。")
                return
            # print(f"{'%03d'%3}")
            path= os.path.join(self.opt.outputPath,"txt",f"{resource.id:0>7d}.txt")
            log.succ (f"[+]保存文件：{path} , 节点数:{len(node_list)}")
            folder=os.path.dirname(path)
             
            final_config =clash.add_proxies_to_model(node_list,{"proxies":[]})  
            if not os.path.exists(folder): os.makedirs(folder)
            clash.save_config(path, final_config)

            # 有 ’+‘ 即为读写模式
            # a 不存在创建，存在追加
            # a+ 追加后读，指针移至末尾
            # w  创建新文件，覆盖
            # w+ 覆盖
            # r  文件必须存在
            # r+  文件必须存在
            '''
            file=open(path,"w",encoding="utf-8")
            updated_list = json.dumps( node_list, sort_keys=False, indent=2, ensure_ascii=False)
            file.writelines(updated_list)
            file.flush()
            file.close()
            '''
        except Exception as e:
           log.err(f"写文件错误:{e}",e)
           pass
             
    def genNode(self,resource:nodeResource)->list:
        nodes_list=[]
        addr=resource.address
        try:
            nodeContent=self._getNodeContent(resource) 
            nodes_list=nodes.parser_content(nodeContent) 
        except Exception as e:
            log.err('[-]解析节点失败:"{}",{}'.format(e,addr),e)
            pass
        return nodes_list

    def __getHttpContent(url,proxy:str=None):
        try:
            response = webutility.get(url,proxy=proxy)  
            #print("Encoding:"+response.apparent_encoding,response.encoding)
            response.encoding="utf-8"
            return response.text 
        except Exception as e:
            log.err(f"[-]http请求'{url}'出现异常：{e}")
            pass

    def _getNodeContent(self,resource:nodeResource)->str:
        '''
        获取节点的文本内容
        '''
        log.info(f"订阅：'{resource.address}'...") 
        content=None
        if(resource.resourceType==resourceType.http):
            content=clash.__getHttpContent(resource.address,self.opt.proxy)
            if content==None and opt.proxy!=None:content=clash.__getHttpContent(resource.address)
            if content==None :return 
        elif(resource.resourceType==resourceType.file):
            filePath=resource.address
            if not os.path.exists(filePath) or not os.path.isfile(filePath):log.warn(f"输入的文件路径'{filePath}'不存在！")
            file=open(filePath,"r",encoding="utf-8") 
            content=file.read()
            file.close() 
        return content
    
    def genNodeList(self,noderesources:list[nodeResource]):  
        '''
        从URL列表中生成节点
        arg: noderesources        base64 url|yaml url node list url
        '''
        # 请求订阅地址
        '''
        #无返回值使用方法
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures={executor.submit(self._genNode,(resource)) for resource in noderesources}
        concurrent.futures.wait(futures,return_when=concurrent.futures.FIRST_COMPLETED)
        '''
        '''
        未知
        #for future in concurrent.futures.as_completed(futures):
        #    future.done()
        '''
       
        node_list=[]
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures={executor.submit(self.genNode,resource):resource for resource in noderesources}
            for future in concurrent.futures.as_completed(futures): 
                resource=futures[future] 
                tlist=future.result()
                if tlist ==None: 
                    log.warn(f'[-]订阅{resource.address} clash节点数:\t0个') 
                    continue
                if self.opt.nodeOutputToFile:self.__saveFile(resource,tlist)
                log.succ(f'[+]订阅{resource.address} clash节点数:\t{len(tlist)}个') 
                node_list.extend(tlist)
        return node_list

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

    @staticmethod
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
    
    def templateConfig(self):
        yamlConfig=clash.getTemplateConfig(self.opt.templateUrl,self.opt.backLocalTemplate,self.opt.proxy)
        return yamlConfig
    
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
        f = 0
     
        for item in nodeList:
            if 'name' in item:
                if 'server' not in item or 'port' not in item: continue
                domain = item['server']
                port = item['port']
                server=f"{domain}:{port}" 
                if server in servers:
                    f+=1
                    #log.warn(f"重复节点：{server}")
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
        log.warn(f"重复节点：{f}个")
        return result
    # 将代理添加到配置文件
    def add_proxies_to_model(nodeList:list, model): 
        if nodeList is None or model is None:
            raise ValueError('Invalid input: data and model cannot be None')
         
        try: 
            if model.get('proxies') is None:model['proxies'] =nodeList
            else:model['proxies'].extend(nodeList)
        except Exception as e:
            log.err(f'Error adding proxies to model: {e}')

        try:
            groups=model.get('proxy-groups')
            if groups != None:
                nodeList = [d for d in model['proxies'] if 'name' in d] 
                nodeNames =[]
                
                for item in nodeList:
                    if item['name'] not in nodeNames:nodeNames.append(item['name'])  
                    #uuidReg="\w{8}[-\w{4}]{3}-\w{12}"#"b74f4afa-1a57-4aff-b7e5-8ad5ea33566f"
                    item['uuid']=str(uuid.uuid3(uuid.NAMESPACE_DNS,item['name'])) # 根据名称生成UUID ，相同名称生成的UUID相同

                for group in groups:
                    if group.get('proxies') is None:
                        #group['proxies'] = data.get('proxy_names')
                        group['proxies'] = nodeNames
                    else:
                        #group['proxies'].extend(data.get('proxy_names'))
                        group['proxies'].extend(nodeNames)
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
        if 'server' not in node or 'port' not in node or 'password' in node:return False 
        domain = node['server']
        domain=domain .strip()
        node['server']=domain
        port = node['port']
        result=tcp.check_tcp_port({"host":domain,"port":port})
        #log.info(f"检测节点结果:{result}")
        status=result["status"]
        if status:
            return True
            delay=tcp.ping(domain) # 在github Action 不支持
            log.info(f"检测网络延迟：{domain}: {delay} ms")
            if delay== None or delay >delay: status= False
        return status
    @staticmethod
    def checkNodes(nodeList,delay:int=1000):
        '''
        检测节点
        '''
        # 去重 
        _nodeList=[]
        s_i=0
        f_i=0
     
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures={executor.submit(clash.checkNode,item,delay):item for item in nodeList}
            for future in concurrent.futures.as_completed(futures): 
                item=futures[future] 
                if(future.result()):
                    _nodeList.append(item)
                    #log.info(f"[+]'{item['server']}:{item['port']}'.")
                    s_i+=1
                else: 
                    #log.info(f"[-]'{item['server']}:{item['port']}'.")
                    f_i+=1
        log.info(f"[+] success:'{s_i}',[-] fail:'{f_i}'.")
        return _nodeList
    
    @staticmethod
    def outputToFile(yamlConfig,nodeList:list,yamlNodeNum:int,outputFolder:str,fileName): 
        log.info(f'[+]节点数...{len(nodeList)}')
        index=math.floor(len(nodeList) / yamlNodeNum)  
        index+=1 if len(nodeList) % yamlNodeNum > 0 else 0
        i=0
        if not os.path.exists(outputFolder):os.makedirs(outputFolder)
        filePath=os.path.join(outputFolder,fileName)
        while i<index:
            ii=i*yamlNodeNum
            jj=(i+1)*yamlNodeNum
            data=nodeList[ii:jj]
            #data["proxy_names"]=[item["name"] for item in data["proxy_list"]] 
          
            #输出文件夹
            if i>0:
                name,ext= os.path.splitext(fileName)
                filePath=os.path.join(outputFolder,name+"_"+str(i)+ext)
            _yamlConfig=copy.deepcopy( yamlConfig )
            final_config =clash.add_proxies_to_model(data, _yamlConfig) 
            clash.save_config(filePath, final_config)
            i+=1
            
    def genYamlForClash(self,yamlNodeNum:int):
        '''
        desc: 生成yaml 文件
        yamlNodeNum: yaml 节点数
        ''' 
        log.start_mark("gen node")
        node_list=self.genNodeList(self.opt.noderesources) 
        log.end_mark("gen node") 

        log.start_mark("remove")
        nodelist=clash.remove_duplicates(node_list)
        log.end_mark("remove") 
        if self.opt.checkNode: nodelist=clash.checkNodes(nodelist) 
        
        log.start_mark("导出配置")
        log.info("获取导出配置模板...")
        yamlConfig=clash.getTemplateConfig(self.opt.templateUrl,self.opt.backLocalTemplate,self.opt.proxy) 
        clash.outputToFile(yamlConfig,nodelist,yamlNodeNum,  self.opt.outputPath,clash._outputYamlFileName)
        log.end_mark("导出配置") 

    def genYaml(self,resource:nodeResource,templateConfig)->None:
        '''
        单个文件输出
        输出文件名为资源id +.yaml
        '''
        log.start_mark("gen node")
        nodes=self.genNode(resource)
        log.end_mark(f"gen node : {len(nodes)}")
        log.start_mark("remove")
        nodelist=clash.remove_duplicates(nodes)
        log.end_mark("remove") 
        if self.opt.checkNode: nodelist=clash.checkNodes(nodelist) 
        log.start_mark("导出配置")
        clash.outputToFile(templateConfig,nodelist,3000,self.opt.outputPath,f"{resource.id}.yaml") 
        log.end_mark("导出配置") 

    def genYamlToFile(self):
        yamlConfig=self.templateConfig( ) 
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures={executor.submit(self.genYaml,r,yamlConfig) for r in self.opt.noderesources}
            '''
            for f in concurrent.futures.as_completed(futures):
                r=f.result()
            '''
            # 等待所有任务完成
            concurrent.futures.wait(futures)

if __name__ == '__main__': 
    opt=clashOption(subArray=["https://tt.vg/evIzX"])
    cl =clash (opt)
    cl.genYamlForClash()



