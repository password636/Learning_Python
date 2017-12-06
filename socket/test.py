import socket

s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
print(s.getdefaulttimeout())
