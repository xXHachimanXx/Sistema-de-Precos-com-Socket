import socket

class Fuel:
    def __init__(self, fuelType, fuelPrice):
        self.fuelType = fuelType
        self.fuelPrice = int(fuelPrice * 1000)
    
    def __str__(self):
        return (self.fuelType + ' ' + self.fuelPrice)

class GasStation:
    def __init__(self, fuels):
        self.fuels = fuels
    

def upServer():    
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # pegar nome da maquina local
    host = socket.gethostname()
    port = 3333

    serversocket.bind((host, port))


def main():
    listOfGasStations = []
    
    with open('gas_stations.txt', 'r') as gasStations:
        for gasStation in gasStations:
            gasStationDetais = gasStation.split(' ')
            
            
        
    # serversocket.listen(5)

    # while True:
    #     clientsocket, addr = serversocket.accept()

    #     print("Got a connection from %s" % str(addr))

    #     msg = 'Thanks for connect' + '\r\n'
    #     clientsocket.send(msg.encode('ascii'))
    #     clientsocket.close()
