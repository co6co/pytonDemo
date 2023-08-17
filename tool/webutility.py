import base64

def safe_decode(s:str)->str:
    print("saft_decode:",s)
    num = len(s) % 4
    if num:s += '=' * (4 - num)
    print(f"s:{s},num:{num}")
    return base64.urlsafe_b64decode(s)