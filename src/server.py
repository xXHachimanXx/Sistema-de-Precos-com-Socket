import socket
from math import sqrt

serversocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
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
                "\nD " + 
                str(idDataMsg) + " " +
                str(msg[1]) + " " +
                str(msg[2]) + " " +
                str(msg[3]) + " " +
                str(msg[4])
            )
            
        idDataMsg += 1
    
    @staticmethod
    def getLowerGasPrice(fuelType, searchRadius, lat, long):
        lowerGasPrice = -1
        lowerGasPriceObject = None
        stationOfLowerlowerGasPriceObject = None
        
        success = False  
        searchRadius = float(searchRadius)      
        
        # Retornar lista de postos dentro do raio de busca
        newListOfGasStations = list(filter(
            lambda elem: 
                pointsDistance(elem.lat, lat, elem.long, long) <= searchRadius,
                
            listOfGasStations
        ))
        
        print("listaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        print(newListOfGasStations)
          
        
        if len(newListOfGasStations) == 0:
            response = "Nenhum posto dentro do raio requisitado."
            
        else:        
            # Iterar na lista de combustíveis de cada posto em busca
            # do menor preço e retorná-lo
            for gs in newListOfGasStations:            
                for gsFuelRequired in gs.fuels:
                    if gsFuelRequired.fuelType == fuelType and gsFuelRequired.fuelPrice < lowerGasPrice:
                        lowerGasPrice = gsFuelRequired.price
                        lowerGasPriceObject = gsFuelRequired
                        stationOfLowerlowerGasPriceObject = gs                        
                        
            success = True   
                    
            if stationOfLowerlowerGasPriceObject == None:
                response = "Não há nenhum posto com este tipo de combustível."
            else:
                response = "Tipo de combustível: " + fuelType + \
                       "\nRaio de busca: " + str(searchRadius) + \
                       "\nCoordenadas do centro: " + str((lat,long)) + \
                       "\nMenor preco: " + str(lowerGasPrice) + \
                       "\nCoordenadas do posto: " + str((stationOfLowerlowerGasPriceObject.lat, stationOfLowerlowerGasPriceObject.long))
            
            
        return (success, response)
        
def pointsDistance(xA, xB, yA, yB):
    absxAB = abs( float(xA) - float(xB) ) ** 2
    absyAB = abs( float(yA) - float(yB) ) ** 2
    return sqrt( absxAB + absyAB )
            
    
def initServer(port):
    """Método para inicializar o servidor e carrgar dados da database.        

        Parameters
        ----------
        port : int
            A porta a ser escutada pelo servidor.
    """
    global serversocket
    
    # pegar nome da maquina local
    host = socket.gethostname()
    
    # conectar e setar tamanho do backlog
    serversocket.bind((host, port))
    
    # carregar dados na memória
    with open('../database/gas_stations.txt', 'r') as gasStations:
        for gasStation in gasStations:
            gasStationDetais = gasStation.split(' ')            
            gasStationDetais.pop(1) # Remover id da mensagem 
            insertIntoListOfGasStations(gasStationDetais)
    
    print("Servidor operante!\n")
    
    
def searchGasStation(lat, long):    
    """Função para procurar um posto de combustível na base de dados.

        Parameters
        ----------
        lat: double
            Latitude do posto.
        long: double
            Longitude do posto.
            
        Returns
        -------
        int
           Índice do posto na lista de postos.
    """
    sgIndex = None
    
    # Iterar na lista de postos de cimbustível até encontrar
    # o índice do posto requisitado
    for idx, gs in enumerate(listOfGasStations):
        if gs.lat == lat and gs.long == long:
            sgIndex = idx            
            break
        
    return sgIndex
            
def insertIntoListOfGasStations(gasStationDetais):        
    
    """Método para inserir posto de combustível na lista de postos.

        Parameters
        ----------
        gasStationDetails : list
            Detalhes do posto de combustível.            
    """
    
    # Procurar um posto de combustível existente
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
    """Função para checar entrada do client.

        Parameters
        ----------
        msg : str
            Mensagem do client.
            
        Returns
        -------
        boolean
           Validez da mensagem
    """
    return (
        len(msg) == 5 and
        (msg[0] == 'D' or msg[0] == 'P')
    )

def consoleWarning(msg, success, address):
    """Método para mostrar a situação da operação.

        Parameters
        ----------
        msg : str
            Mensagem do client.
        success : boolean
            Flag de sucesso/fracasso da operação.
        client : socket
            Objeto que representa o client da operação.
    """
    successFlag = "Sucesso"
    
    if not success:        
        successFlag = "Fracasso"
        
    print(
        "Client: " + address[0] + ":" + str(address[1]) +
        "\nTipo de mensagem: " + msg[0] +
        "\nStatus: " + successFlag
    )
    

def main():
    print("Bem-vindo ao servidor do Sistema de Preços!")
    port = int(input("Digite a porta a ser escutada pelo servidor para inicializá-lo: "))
    
    initServer(port)

    while True:
        global listOfGasStations
        global serversocket
        success = False
        
        msg, client = serversocket.recvfrom(1024)        
        msg = msg.decode('utf-8').split(' ')
        
        if(checkInput(msg)):
            
            # cadastro
            if msg[0] == 'D':
                print("Mensagem recebida!\n")
                insertIntoListOfGasStations(msg)
                GasStation.saveOnDatabase(msg)
                success = True
                consoleWarning(msg, success, client)
                serversocket.sendto("Cadastro realizado!".encode('utf-8'), client)
            
            # pesquisa
            if msg[0] == 'P':
                print("Mensagem recebida!\n")
                success, resp = GasStation.getLowerGasPrice(
                    msg[1], msg[2], msg[3], msg[4]
                )
                consoleWarning(msg, success, client)
                
                serversocket.sendto(resp.encode('utf-8'), client)
        else:            
            consoleWarning(msg, success, client)
            serversocket.sendto(
                "Server - Erro: Entrada de dados inválida!".encode("utf-8"),
                client
            )

    # Fechar conexao
    serversocket.close()

main()