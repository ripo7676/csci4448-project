from GameObservable import *
from PieceFactory import *
from Space import *
from PieceFactory import *
import numpy as np

class CheckersBoard(GameObservable):

    def __init__(self):
        self.observers = []
        self.numRows = 8
        self.numCols = 8
        self.spaces = [[Space(locationJ=j, locationI=i) for i in range(0, self.numCols)] for j in range(0, self.numRows)]
        self.moveOptions = [{'moveLeft':(1,1), 'moveRight':(1,-1), 'jumpLeft':(2,2), 'jumpRight':(2,-2)}, {'moveLeft':(-1,-1), 'moveRight':(-1,1), 'jumpLeft':(-2,-2), 'jumpRight':(-2,2)}]

    def initializeGameBoard(self):
        assert (len(self.observers) == 2), 'Must have two players to start game'

        pieceCounter = 0
        for i in range(0, 3):
            for j in range(0, self.numCols, 2):
                if ((i % 2) == 0):
                    # initialize player1 pieces for even rows
                    self.observers[0].addToPieceCollection('X{0:02d}'.format(pieceCounter), CheckersPiece(ID='X{0:02d}'.format(pieceCounter), owner=self.observers[0], location=(i, j+1)))
                    self.spaces[i][j+1].setSpaceResident(self.observers[0].getPieceFromCollection('X{0:02d}'.format(pieceCounter)))

                    # initialize player2 pieces for even rows
                    self.observers[1].addToPieceCollection('O{0:02d}'.format(pieceCounter), CheckersPiece(ID='O{0:02d}'.format(pieceCounter), owner=self.observers[1], location=(7-i, j)))
                    self.spaces[7-i][j].setSpaceResident(self.observers[1].getPieceFromCollection('O{0:02d}'.format(pieceCounter)))
                else:
                    # initialize player1 pieces for odd rows
                    self.observers[0].addToPieceCollection('X{0:02d}'.format(pieceCounter), CheckersPiece(ID='X{0:02d}'.format(pieceCounter), owner=self.observers[0], location=(i, j)))
                    self.spaces[i][j].setSpaceResident(self.observers[0].getPieceFromCollection('X{0:02d}'.format(pieceCounter)))
                    # initialize player2 pieces for odd rows
                    self.observers[1].addToPieceCollection('O{0:02d}'.format(pieceCounter), CheckersPiece(ID='O{0:02d}'.format(pieceCounter), owner=self.observers[1], location=(7-i, j+1)))
                    self.spaces[7-i][j+1].setSpaceResident(self.observers[1].getPieceFromCollection('O{0:02d}'.format(pieceCounter)))

                pieceCounter += 1

        for observer in self.observers:
            observer.setNumPieces()

    def getState(self):
        pass

    def setState(self, newState):
        pass

    def getSpaceByLocation(self, rowIndex, columnIndex):
        returnSpace = None
        if (rowIndex >= 0 and columnIndex < len(self.spaces)) and (rowIndex >= 0 and columnIndex < len(self.spaces[0])):
            returnSpace = self.spaces[rowIndex][columnIndex]
        return returnSpace

    def isValidMove(self, player, currentLocation, moveType):
        vertical, horizontal = self.moveOptions[self.observers.index(player)][moveType]
        if ((currentLocation[0]+vertical > self.numRows) or (currentLocation[0]+vertical < 0)):
            return False
        elif ((currentLocation[1]+horizontal > self.numCols) or (currentLocation[1]+horizontal < 0)):
            return False
        else:
            if (moveType == 'jumpLeft' or moveType == 'jumpRight'):
                jumpedSpace = self.getSpaceByLocation(int(currentLocation[0]+vertical/2),  int(currentLocation[1]+horizontal/2))
                if ((jumpedSpace.getSpaceResident() != player) and (jumpedSpace.getSpaceResident() is not None)):
                    return True
            else:
                return True
        return False

    def movePlayerPiece(self, piece, player, currentLocation, moveType):
        vertical, horizontal = self.moveOptions[self.observers.index(player)][moveType]
        if self.isValidMove(player, currentLocation, moveType):
            if (moveType == 'jumpLeft' or moveType == 'jumpRight'):
                # remove opponent piece, move piece
                jumpedSpace = self.getSpaceByLocation(int(currentLocation[0]+vertical/2),  int(currentLocation[1]+horizontal/2))
                #TODO: decrement opponent player's piececount
                jumpedSpace.getSpaceResident().getOwner().decrementNumPieces()
                jumpedSpace.removeSpaceResident()

            self.getSpaceByLocation(currentLocation[0], currentLocation[1]).removeSpaceResident()
            self.getSpaceByLocation(currentLocation[0]+vertical, currentLocation[1]+horizontal).setSpaceResident(piece)
            currentLocation = (currentLocation[0]+vertical, currentLocation[1]+horizontal)
        else:
            print('invalid move')

        self.notifyObservers()

        return currentLocation

    def getReadOnlyState(self):
        return ([['---' if (space.getSpaceResident() is None) else space.getSpaceResident().getID() for space in row] for row in self.spaces])

    #for testing
    def printBoard(can):
		#prototype gui checkerboard
		w=can.winfo_width()
		h=can.winfo_height()
		cellwidth = w/8
		cellheight = h/8
		for row in range(8):
			for col in range(8):
				if (row+col)%2 == 0:
					can.create_rectangle(col*cellwidth, row*cellheight, (col+1)*cellwidth, (row+1)*cellheight, fill = 'black')
				else:
					can.create_rectangle(col*cellwidth, row*cellheight, (col+1)*cellwidth, (row+1)*cellheight, fill = 'red')	
        #for row in self.spaces:
         #   print(['---' if (space.getSpaceResident() is None) else space.getSpaceResident()._ID for space in row])
        #print()
        
					
window = Tk()
thecanvas = Canvas(window, width=500, height=500)
thecanvas.grid(row=0, column=0)
window.update_idletasks()
printBoard(thecanvas)
window.mainloop

