from Server import *

class GameServer(Server):
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.connections = []
        self.serverSocket = socket.socket()
        self.serverSocket.bind((self.address, self.port))
        self.serverSocket.listen()

    def notify(self):
        for clientSocket, clientConnection in self.connections:
            clientConnection.send(bytes("You have been connected", 'utf-8'))
            print(str(clientSocket.recv(1024), 'utf-8'))

server = GameServer(socket.gethostbyname(''), 1234)
client = socket.socket()
server.addConnection(client)
server.notify()
client.close()
server.serverSocket.close()
