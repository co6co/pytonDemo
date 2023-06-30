import re

class base64: 
    def isBase64(content):
        _reg="^([A-Za-z0-9+/]{4})*([A-Za-z0-9+/]{4}|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{2}==)$"
        group=re.match(_reg,content)
        if group !=None:return True
