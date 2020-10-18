import socket 

# criar um objeto socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# pegar nome da maquina local
host = socket.gethostname()
port = 3333

s.connect((host, port))

# limitar mensagens para ate' 1024 bytes
msg = s.recv(1024)

s.close() # fechar conexao
print(msg.decode('ascii')) # printar mensagem decodificada
