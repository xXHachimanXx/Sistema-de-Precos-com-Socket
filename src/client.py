import socket 
import ipaddress

# criar um objeto socket
udpConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Método para testar conexão
def testIp(destiny):    
    ip = destiny[0]

    res = True
    # testar ip
    try:
        ip = ipaddress.ip_address(ip)        
    except ValueError:
        res = False
    
    return res    

# Ler dados do usuário
def readClientData():
    
    while True:
        destiny = input("Informe o ip e a porta da seguinte forma: <ip> <porta>\n").split(' ')
        
        if destiny[0] == "localhost":
            hostname = socket.gethostname()
            destiny[0] = socket.gethostbyname(hostname)

        if len(destiny) == 2 and testIp(destiny):
            break
        else:      
            print(destiny)      
            print("Ip ou porta inválida! Tente de novo: ")

    return destiny


def main():
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
            continue
        
        msg = flag.encode("utf-8")
        
        udpConnection.sendto(msg, (host, port))
        
        udpConnection.settimeout(5.0)
        msg, client = udpConnection.recvfrom(1024)
        
        if msg:
            print(msg.decode('utf-8'))            
                    

main()