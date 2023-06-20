import base64

def safe_decode(s):
    print("saft_decode:",s)
    num = len(s) % 4
    if num:
        s += '=' * (4 - num)
    return base64.urlsafe_b64decode(s)