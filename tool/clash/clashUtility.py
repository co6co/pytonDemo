import requests,base64,yaml,sys,os
sys.path.append(os.path.abspath( os.path.join( os.path.dirname(__file__),".."))) #引入log所在绝对目录
from log import log,logger
import webutility
from convert2clash import *
from parserNode import *


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
            yml = yaml.load(content, Loader=yaml.FullLoader)
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
          
    def genNodeList(self,urlList): #生成 proxy_list 
        # 请求订阅地址
        for url in urlList:
            log("订阅：'{}'".format(url))
            response = webutility.get(url)
            print(f"https://tt.vg/evIzX:{response.status_code}")
            response=response.text
            try:
                raw = base64.b64decode(response)
                self.parseNodeText(raw)
            except Exception as e:
                log('base64解码失败:"{}",应当为clash节点'.format(e))
                log('clash节点提取中...')
                self.parseYaml(response) 

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
        except requests.exceptions.RequestException:
            log(f'网络获取规则{url}配置模板失败,加载本地配置文件')
            template_config =clash.load_local_config(path)
        log('已获取规则配置文件')
        return template_config
    
    #去重
    def remove_duplicates(lst):
        result = []
        namesl = []
        i = 1
        for item in lst:
            if 'name' in item:
                domain = item['server']

                pattern = '[^\u4e00-\u9fa5\d]+'
                item['name'] = re.sub(pattern, '', item['name'])
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
                    print(item['name'])
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

    def genYamlForClash(self):
        config_path = self.opt.backLocalTemplate
        clashOpt=self.opt
        yamlConfig=self.getTemplateConfig(clashOpt.templateUrl,config_path)
        self.genNodeList(self.opt.subUrlArray)
        log(f'通过模板导出配置文件...')
        final_config =clash.add_proxies_to_model(self.proxy_list, yamlConfig) 
        print(f'文件已导出至 {clashOpt.outputPath}')
        clash.save_config(clashOpt.outputPath, final_config)
        

class clashOption():
    def __init__(self,subArray=list):
    
        #模板 __xxxx 私有属性不能被继承
        self.__templateUrl="https://raw.githubusercontent.com/w1770946466/Auto_proxy/main/config.yaml" 
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



