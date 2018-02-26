import socket

connection = socket.socket()
connection.connect(('127.0.0.1', 10000))

connection.send(b'Hello from client\n')
data = b''
recv = connection.recv(1024)
while recv:
    data += recv
    recv = connection.recv(1024)
print (data.decode('utf-8'))
connection.close()