#!/usr/bin/env python
import ctypes
so = ctypes.CDLL('./libwebsockets.so')

print ("666")
print("send: " + so.send("AAPH,80010002,123,message"))
