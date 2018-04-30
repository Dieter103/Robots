import socket
HOST = '10.200.48.128'
PORT = 8888

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('socket created')


try:
    s.bind((HOST, PORT))
except socket.error as err:
    print ('Bind Failed, Error Code')
    sys.exit()

print ('Socket Bind Success!')

s.listen(1000)
print ('Socket is now listening')

while 1:
    conn, addr = s.accept()
    print ('Connect with ' + addr[0] + ':' + str(addr[1]))
    buf = conn.recv(64)
    print (buf)
s.close()
