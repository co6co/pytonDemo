import urllib.parse,json
import optparse
from anonBrowser import *

class Google_Result:
    def __init__(self,title,text,url):
        self.title = title
        self.text = text
        self.url = url
    def __repr__(self):
        return self.title
      
def google(search_term):

    ab = anonBrowser(proxies= [ "127.0.0.1:9666"])
    search_term = urllib.parse.quote_plus(search_term)
    # 过时了
    response =    ab.open('http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=' + search_term)
 
    objects = json.load(response)
    results = []
    for result in objects['responseData']['results']:
        url = result['url']
        title = result['titleNoFormatting']
        text = result['content']
        new_gr = Google_Result(title, text, url)
        results.append(new_gr)
    return result

def main():
    parser = optparse.OptionParser('usage%prog -k <target url>')
    parser.add_option('-k', dest='key', type='string', help='specify    target url') 

    (options, args) = parser.parse_args()
    key = options.key 
    if key == None:
        print (parser.usage)
        exit(0)
    else:
        google(key)

if __name__ == '__main__':
    main()
