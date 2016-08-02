#-*- coding: utf-8 -*-

import binascii
f=open('response.dat','rb')
a=f.read()
print(a)
hexstr=binascii.b2a_hex(a)
bsstr=bin(int(hexstr,16))#[2:]
print(hexstr)
print(bsstr)
aaa=binascii.a2b_hex(hexstr)
print(aaa)