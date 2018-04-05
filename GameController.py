from CheckersBoard import *
from RemoteCheckersBoard import *
from HumanPlayer import *
from Server import *
from ClientSocket import *
#from GameState import *

import time

class GameController:
    def __init__(self):
        self.game = None
        #self.view = view

    def setGame(self, newGame):
        self.game = newGame

    def hostGame(self, user):
        self.setGame(RemoteCheckersBoard(Server(socket.gethostbyname(''), 10000)))
        self.game.getServer().run()
        user.commSocket = ClientSocket(socket.gethostbyname(''), 10000, 1)
        while (self.game.getServer().getNumberOfClientConnections() < 2):
            print("waiting for user to join...")
            time.sleep(2)
        self.runRemoteGame(user)

    def joinGame(self, user):
        user.commSocket = ClientSocket(socket.gethostbyname(''), 10000, 2)
        while True:
            pieceID = input("pieceID: ")
            moveType = input("moveType: ")
            user.commSocket.clientSocket.send(pickle.dumps(('joiningUser', pieceID, moveType)))

    def runRemoteGame(self, user):
        self.game.addObserver(HumanPlayer('1'))
        self.game.addObserver(HumanPlayer('2'))
        self.game.initializeGameBoard()
        self.game.broadcastState()

        while(max(self.game.observers[0].getNumPieces(), self.game.observers[1].getNumPieces()) > 0):

            pieceID = input("pieceID: ")
            moveType = input("moveType: ")
            user.commSocket.clientSocket.send(pickle.dumps(('hostingUser', pieceID, moveType)))

            while (len(self.game.getServer().commandQueue['hostingUser']) < 1):
                continue

            pieceToMove, moveType = self.game.getServer().commandQueue['hostingUser'].pop(0)
            self.game.observers[0].makeMove(self.game, pieceToMove, moveType)
            self.game.broadcastState()

            while (len(self.game.getServer().commandQueue['joiningUser']) < 1):
                continue

            pieceToMove, moveType = self.game.getServer().commandQueue['joiningUser'].pop(0)
            self.game.observers[1].makeMove(self.game, pieceToMove, moveType)
            self.game.broadcastState()


    def playAI(self, humanPlayer):
        #self.setGame(CheckersBoard())
        #self.game.addObserver(humanPlayer)
        #self.game.addObserver(AIPlayer())
        pass

    def runLocalGame(self):
        self.game.initializeGameBoard()
        self.game.printBoard()

        while(max(self.game.observers[0].getNumPieces(), self.game.observers[1].getNumPieces()) > 0):
            for player in self.game.observers:
                pieceID = input("Piece ID: ")
                moveType = input("Move Type: ")
                player.makeMove(self.game, pieceID, moveType)

'''
newGame = GameController()
newGame.setGame(CheckersBoard())
player1 = HumanPlayer('1')
player2 = HumanPlayer('2')
newGame.game.addObserver(player1)
newGame.game.addObserver(player2)
newGame.runLocalGame()
'''
