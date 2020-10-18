import socket

# criando um objeto socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# pegar nome da maquina local
host = socket.gethostname()
port = 3333

serversocket.bind((host, port))

serversocket.listen(5)

while True:
    clientsocket, addr = serversocket.accept()

    print("Got a connection from %s" % str(addr))

    msg = 'Thanks for connect' + '\r\n'
    clientsocket.send(msg.encode('ascii'))
    clientsocket.close()
