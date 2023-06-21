import requests, yaml,base64,os
def get_proxies(urls):
    url_list = urls.split(';')
    
  
    headers=   {"User-agent":"'Mozilla/5.0 (X11; U; Linux 2.4.2-2 i586;en-US; m18) Gecko/20010131 Netscape6/6.01"}
    hideMeProxy={'socks5':"127.0.0.1:9666"}
    proxy_list = {
        'proxy_list': [],
        'proxy_names': []
    }
    # 请求订阅地址
    for url in url_list:
        print(url)
        response = requests.get(url, headers=headers, timeout=5000).text
        try:
            raw = base64.b64decode(response)
            print(raw)
        except Exception as e:
            print(e)
            pass
        nodes_list = raw.splitlines() 
        for node in nodes_list:
            print(node)



def main():
    url="https://moes.lnaspiring.com/Moe233-Subs/wel/api/v1/client/subscribe?token=2aeb6746f02ff8ca02a891cc0f43cbe4"
    get_proxies(url)

if __name__ == "__main__":
    main()