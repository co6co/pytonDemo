# coding=UTF-8
__author__='cy'

import pexpect
PROMPT=['#','>>>','>','\$']

def send_command(child,cmd):
    child.sendline(cmd)
    child.expect(PROMPT)
    print(child.before)

def connect(host,user,password):
    ssh_newkey="Are you sure want to continue connecting"
    connStr ='ssh'+user+'@'+host
    child =pexpect.spawn(connStr)
    ret =child.expect([pexpect.TIMEOUT,ssh_newkey,'[P|p]assword:'])
    
    if ret == 0:
        print('- Error Connecting')
        return 
    if ret ==1:
        child.sendline("yes")
        ret =child.expect([pexpect.TIMEOUT,ssh_newkey,'[P|p]assword:'])
    if ret == 0:
        print('- Error Connecting')
        return 
    child.sendline(password)
    child.expect(PROMPT)
    return child
