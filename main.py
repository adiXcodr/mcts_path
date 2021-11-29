
from copy import deepcopy
from algorithm.mcts import mcts
from algorithm.utils import initialBoard
from functools import reduce
import operator
import numpy as np

DIMENSION = 3

class mazeEnvironmentState():
    def __init__(self):
        self.board = initialBoard(DIMENSION)
        self.currentPlayer = 0

    def changeCurrentPlayer(self,player):
        self.currentPlayer = player

    def changeBoard(self,x,y):
        newState = deepcopy(self)
        newState.board[x][y] = self.currentPlayer
        self.board = newState.board

    def displayBoard(self):
        print("Interation",self.currentPlayer)
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.board]))
        print("")

    def getCurrentPlayer(self):
        return self.currentPlayer

    def getPossibleActions(self):
        possibleActions = []
        b=np.array(self.board)
        max_index= np.unravel_index(b.argmax(), b.shape)
        if(max_index[0]==0):
            if (max_index[1]==0):
                if(self.board[0][1]!=-1):
                    possibleActions.append(Action(player=self.currentPlayer, x=0, y=1))
                if(self.board[1][0]!=-1):
                    possibleActions.append(Action(player=self.currentPlayer, x=1, y=0))
            elif(max_index[1]==2):
                if(self.board[0][1]!=-1):
                    possibleActions.append(Action(player=self.currentPlayer, x=0, y=1))
                if(self.board[1][2]!=-1):    
                    possibleActions.append(Action(player=self.currentPlayer, x=1, y=2))
            else:
                if(self.board[max_index[0]][max_index[1]-1]!=-1):
                    possibleActions.append(Action(player=self.currentPlayer, x=max_index[0], y=max_index[1]-1))
                if(self.board[max_index[0]][max_index[1]+1]!=-1):
                    possibleActions.append(Action(player=self.currentPlayer, x=max_index[0], y=max_index[1]+1))
                if(self.board[max_index[0]+1][max_index[1]+1]!=-1):
                    possibleActions.append(Action(player=self.currentPlayer, x=max_index[0]+1, y=max_index[1]+1))

        elif(max_index[0]==2):
            if (max_index[1]==0):
                if(self.board[2][1]!=-1):
                    possibleActions.append(Action(player=self.currentPlayer, x=2, y=1))
                if(self.board[1][0]!=-1):
                    possibleActions.append(Action(player=self.currentPlayer, x=1, y=0))
            elif(max_index[1]==2):
                if(self.board[2][1]!=-1):
                    possibleActions.append(Action(player=self.currentPlayer, x=2, y=1))
                if(self.board[1][2]!=-1):
                    possibleActions.append(Action(player=self.currentPlayer, x=1, y=2))
            else:
                if(self.board[max_index[0]][max_index[1]-1]!=-1):
                    possibleActions.append(Action(player=self.currentPlayer, x=max_index[0], y=max_index[1]-1))
                if(self.board[max_index[0]][max_index[1]+1]!=-1):
                    possibleActions.append(Action(player=self.currentPlayer, x=max_index[0], y=max_index[1]+1))
                if(self.board[max_index[0]-1][max_index[1]-1]!=-1):
                    possibleActions.append(Action(player=self.currentPlayer, x=max_index[0]-1, y=max_index[1]-1))

        else:
            if(max_index[1]==0):
                if(self.board[max_index[0]][max_index[1]+1]!=-1):
                    possibleActions.append(Action(player=self.currentPlayer, x=max_index[0], y=max_index[1]+1))
                if(self.board[max_index[0]+1][max_index[1]]!=-1):
                    possibleActions.append(Action(player=self.currentPlayer, x=max_index[0]+1, y=max_index[1]))
                if(self.board[max_index[0]-1][max_index[1]]!=-1):
                    possibleActions.append(Action(player=self.currentPlayer, x=max_index[0]-1, y=max_index[1]))

            elif(max_index[1]==2):
                if(self.board[max_index[0]][max_index[1]-1]!=-1):
                    possibleActions.append(Action(player=self.currentPlayer, x=max_index[0], y=max_index[1]-1))
                if(self.board[max_index[0]+1][max_index[1]]!=-1):
                    possibleActions.append(Action(player=self.currentPlayer, x=max_index[0]+1, y=max_index[1]))
                if(self.board[max_index[0]-1][max_index[1]]!=-1):
                    possibleActions.append(Action(player=self.currentPlayer, x=max_index[0]-1, y=max_index[1]))

            else:
                if(self.board[max_index[0]][max_index[1]-1]!=-1):
                    possibleActions.append(Action(player=self.currentPlayer, x=max_index[0], y=max_index[1]-1))
                if(self.board[max_index[0]][max_index[1]+1]!=-1):
                    possibleActions.append(Action(player=self.currentPlayer, x=max_index[0], y=max_index[1]+1))
                if(self.board[max_index[0]+1][max_index[1]]!=-1):
                    possibleActions.append(Action(player=self.currentPlayer, x=max_index[0]+1, y=max_index[1]))
                if(self.board[max_index[0]-1][max_index[1]]!=-1):
                    possibleActions.append(Action(player=self.currentPlayer, x=max_index[0]-1, y=max_index[1]))

        return possibleActions


    def takeAction(self, action):
        newState = deepcopy(self)
        newState.board[action.x][action.y] = action.player
        newState.currentPlayer = self.currentPlayer +1
        return newState

    def isTerminal(self):
        if(self.board[0][DIMENSION-1] !=0):
            return True
        else:
            return False

    def getReward(self):
        for row in self.board:
            if abs(sum(row)) == DIMENSION:
                return sum(row) / DIMENSION
        for column in list(map(list, zip(*self.board))):
            if abs(sum(column)) == DIMENSION:
                return sum(column) / DIMENSION
        # for diagonal in [[self.board[i][i] for i in range(len(self.board))],
        #                  [self.board[i][len(self.board) - i - 1] for i in range(len(self.board))]]:
        #     if abs(sum(diagonal)) == DIMENSION:
        #         return sum(diagonal) / DIMENSION
        return False


class Action():
    def __init__(self, player, x, y):
        self.player = player
        self.x = x
        self.y = y

    def __str__(self):
        return str((self.x, self.y))

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.__class__ == other.__class__ and self.x == other.x and self.y == other.y and self.player == other.player

    def __hash__(self):
        return hash((self.x, self.y, self.player))

if __name__=="__main__":
    play = mazeEnvironmentState()
    searcher = mcts(timeLimit=1000)
    epochs = DIMENSION*DIMENSION+1

    print("Initial Position")
    play.displayBoard()

    #Start player at the starting position at the maze
    play.changeCurrentPlayer(1)
    play.changeBoard(DIMENSION-1,0)

    for i in range(1,epochs-1):
        play.displayBoard()
        try:
            #Update score on board as the current position of the player
            play.changeCurrentPlayer(i+1)
            action = searcher.search(initialState=play)
            print("Moving to",action)
            play.changeBoard(action.x,action.y)
        except Exception as e:
            print("Game Ended!")
            break


