import socket

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listOfGasStations = []
idDataMsg = 0

class Fuel:
    def __init__(self, fuelType, fuelPrice):
        self.fuelType = fuelType
        self.fuelPrice = int(fuelPrice * 1000)
    
    def __str__(self):
        return (self.fuelType + ' ' + self.fuelPrice)

class GasStation:
    def __init__(self, fuels, lat, long):
        self.fuels = fuels # lista de combustíveis vendidos
        self.lat = lat # latitude
        self.long = long # longitude
        
    def insertFuel(self, fuel):
        self.fuels.append(fuel)
                
    def __str__(self):
        str = ""
        
        for fuel in self.fuels:
            str += (fuel + " " + self.lat + " " + self.long + "\n")
            
        return str
    
    @staticmethod    
    def saveOnDatabase(msg):
        global idDataMsg
        with open('../database/gas_stations.txt', 'a', encoding='utf-8') as database:            
            database.write(
                "D " + 
                str(idDataMsg) + " " +
                str(msg[1]) + " " +
                str(msg[2]) + " " +
                str(msg[3]) + " " +
                str(msg[4])
            )
            
        idDataMsg += 1

def initServer(port):
    global serversocket
    
    # pegar nome da maquina local
    host = socket.gethostname()    

    serversocket.bind((host, port))
    serversocket.listen(5)
    # carregar dados na memória
    with open('../database/gas_stations.txt', 'r') as gasStations:
        for gasStation in gasStations:
            gasStationDetais = gasStation.split(' ')            
            gasStationDetais.pop(1) # Remover id da mensagem 
            insertIntoListOfGasStations(gasStationDetais)
    
    print("Servidor operante!")
    
    
def searchGasStation(lat, long):    
    sgIndex = None
    
    for idx, gs in enumerate(listOfGasStations):
        if gs.lat == lat and gs.long == long:
            sgIndex = idx            
            break
            
def insertIntoListOfGasStations(gasStationDetais):        
    
    objGasStationIndex = searchGasStation(
        lat=gasStationDetais[3],
        long=gasStationDetais[4]
    )
    
    # combustivel a ser catalogado
    newFuel = Fuel(fuelType=gasStationDetais[1], 
                   fuelPrice=gasStationDetais[2])
    
    if objGasStationIndex == None:
        # Criar novo posto caso nao exista
        objGasStation = GasStation(
            [newFuel],
            lat=gasStationDetais[3],
            long=gasStationDetais[4]
        )
        # inserir na lista
        listOfGasStations.append(objGasStation)
    else:
        listOfGasStations[objGasStationIndex].insertFuel(newFuel)
    
def checkInput(msg):    
    return (
        len(msg) == 5 and
        (msg[0] == 'D' or msg[0] == 'P')
    )

def main():
    print("Bem-vindo ao servidor do Sistema de Preços!")
    port = int(input("Digite a porta a ser escutada pelo servidor para inicializá-lo: "))
    
    initServer(port)

    while True:
        global listOfGasStations
        global serversocket
        
        client, address = serversocket.accept()
        
        msg = client.recv(1024).decode('utf-8')        
    
        msg = msg.split(' ')
        
        if(checkInput(msg)):
            
            # cadastro
            if msg[0] == 'D':
                insertIntoListOfGasStations(msg)
                GasStation.saveOnDatabase(msg)
                print(
                    "Client: " + client + " " +
                    "Tipo de mensagem: " + msg[0] + " "
                    "Status: Sucesso"                    
                )
                serversocket.sendto("Cadastro realizado!".encode('utf-8'), client)
            
            # pesquisa
            if msg[0] == 'P':
                print(
                    "Client: " + client + " " +
                    "Tipo de mensagem: " + msg[0] + " "
                    "Status: Sucesso"
                )
                serversocket.sendto("Pesquisa realizada".encode('utf-8'), client)
        else:
            print(
                    "Client: " + client + " " +
                    "Tipo de mensagem: " + msg[0] + " "
                    "Status: Fracasso" +
                    "Mensagem: " + ' '.join([str(elem) for elem in msg])
                )
            serversocket.sendto(
                "Server - Erro: Entrada de dados inválida!".encode("utf-8"),
                client
            )
            
    # Fechar conexao
    serversocket.close()
    
main()

