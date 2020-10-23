import socket 
import ipaddress

# criar um objeto socket
udpConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Método para testar conexão
def testConnection(destiny):
    ip = destiny[0]
    port = destiny[1]

    # testar conexao
    res = udpConnection.connect_ex((ip, port))
    udpConnection.close()

    return len(input) == 2 and res == 0

# Ler dados do usuário
def readClientData():
    
    while True:
        destiny = input().split(" ")

        if testConnection(destiny):
            break
        else:
            print("Ip ou porta inválida! Tente de novo: ")

    return destiny


def main():
    print("Informe o ip e a porta da seguinte forma: <ip> <porta>\n")
    destiny = readClientData()
    
    host = str(destiny[0])
    port = int(destiny[1])
    
    flagToExit = False
    print("Entre com um código: ")
    print("D - Cadastrar um posto")        
    print("P - Pesquisar um posto")            
    print("E - Sair da aplicação")
    
    while not flagToExit:
        flag = input()
        
        # testar se e' uma flag de saida
        if flag == "E":
            flagToExit = True
            print('Obrigado e até logo :)')
            pass
        
        msg = flag.encode("utf-8")
        
        udpConnection.sendto(msg, destiny)
        
        udpConnection.settimeout(5.0)
        msg, client = udpConnection.recvfrom(1024)
        
        if msg:
            print(msg.decode('utf-8'))            
        
    
        
    
    
    
    udpConnection.connect((host, port))
    
    # limitar mensagens para ate' 1024 bytes
    msg = udpConnection.recv(1024)
    
    udpConnection.close() # fechar conexao
    print(msg.decode('ascii')) # printar mensagem decodificada
