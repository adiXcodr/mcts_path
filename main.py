
from copy import deepcopy
from algorithm.mcts import mcts
from algorithm.utils import initialBoard
from gui import UserInterface
import operator
import numpy as np

DIMENSION = int(input("Enter Dimension: "))

class mazeEnvironmentState():
    def __init__(self):
        self.board = initialBoard(DIMENSION)
        self.pointer = 0

    def changePointer(self,player):
        self.pointer = player

    def changeBoard(self,x,y):
        newState = deepcopy(self)
        newState.board[x][y] = self.pointer
        self.board = newState.board

    def displayBoard(self,ui):
        print("Interation",self.pointer)
        # print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.board]))
        # print("")
        ui.display_table(self.board)
        ui.run_loop()

    def getCurrentPointer(self):
        return self.pointer

    def getPossibleActions(self):
        possibleActions = []
        b=np.array(self.board)
        max_index= np.unravel_index(b.argmax(), b.shape)

        #First Row
        if(max_index[0]==0):
            #Top Left Corner
            if (max_index[1]==0):
                if(self.board[0][1]!=-1):
                    possibleActions.append(Action(player=self.pointer, x=0, y=1))
                if(self.board[1][0]!=-1):
                    possibleActions.append(Action(player=self.pointer, x=1, y=0))
            #Top Right Corner
            elif(max_index[1]==DIMENSION-1):
                if(self.board[0][DIMENSION-2]!=-1):
                    possibleActions.append(Action(player=self.pointer, x=0, y=DIMENSION-2))
                if(self.board[1][DIMENSION-1]!=-1):    
                    possibleActions.append(Action(player=self.pointer, x=1, y=DIMENSION-1))
            #Rest Top Positions
            else:
                if(self.board[max_index[0]][max_index[1]-1]!=-1):
                    possibleActions.append(Action(player=self.pointer, x=max_index[0], y=max_index[1]-1))
                if(self.board[max_index[0]][max_index[1]+1]!=-1):
                    possibleActions.append(Action(player=self.pointer, x=max_index[0], y=max_index[1]+1))
                if(self.board[max_index[0]+1][max_index[1]]!=-1):
                    possibleActions.append(Action(player=self.pointer, x=max_index[0]+1, y=max_index[1]))

        #Last Row
        elif(max_index[0]==DIMENSION-1):
            #Bottom Left Corner
            if (max_index[1]==0):
                if(self.board[DIMENSION-1][1]!=-1):
                    possibleActions.append(Action(player=self.pointer, x=DIMENSION-1, y=1))
                if(self.board[DIMENSION-2][0]!=-1):
                    possibleActions.append(Action(player=self.pointer, x=DIMENSION-2, y=0))
            #Bottom Right Corner
            elif(max_index[1]==DIMENSION-1):
                if(self.board[DIMENSION-1][DIMENSION-2]!=-1):
                    possibleActions.append(Action(player=self.pointer, x=DIMENSION-1, y=DIMENSION-2))
                if(self.board[DIMENSION-2][DIMENSION-1]!=-1):
                    possibleActions.append(Action(player=self.pointer, x=DIMENSION-2, y=DIMENSION-1))
            #Rest of the last row positions
            else:
                if(self.board[max_index[0]][max_index[1]-1]!=-1):
                    possibleActions.append(Action(player=self.pointer, x=max_index[0], y=max_index[1]-1))
                if(self.board[max_index[0]][max_index[1]+1]!=-1):
                    possibleActions.append(Action(player=self.pointer, x=max_index[0], y=max_index[1]+1))
                if(self.board[max_index[0]-1][max_index[1]]!=-1):
                    possibleActions.append(Action(player=self.pointer, x=max_index[0]-1, y=max_index[1]))

        #Middle Rows
        else:
            if(max_index[1]==0):
                if(self.board[max_index[0]][max_index[1]+1]!=-1):
                    possibleActions.append(Action(player=self.pointer, x=max_index[0], y=max_index[1]+1))
                if(self.board[max_index[0]+1][max_index[1]]!=-1):
                    possibleActions.append(Action(player=self.pointer, x=max_index[0]+1, y=max_index[1]))
                if(self.board[max_index[0]-1][max_index[1]]!=-1):
                    possibleActions.append(Action(player=self.pointer, x=max_index[0]-1, y=max_index[1]))

            elif(max_index[1]==DIMENSION-1):
                if(self.board[max_index[0]][max_index[1]-1]!=-1):
                    possibleActions.append(Action(player=self.pointer, x=max_index[0], y=max_index[1]-1))
                if(self.board[max_index[0]+1][max_index[1]]!=-1):
                    possibleActions.append(Action(player=self.pointer, x=max_index[0]+1, y=max_index[1]))
                if(self.board[max_index[0]-1][max_index[1]]!=-1):
                    possibleActions.append(Action(player=self.pointer, x=max_index[0]-1, y=max_index[1]))

            else:
                if(self.board[max_index[0]][max_index[1]-1]!=-1):
                    possibleActions.append(Action(player=self.pointer, x=max_index[0], y=max_index[1]-1))
                if(self.board[max_index[0]][max_index[1]+1]!=-1):
                    possibleActions.append(Action(player=self.pointer, x=max_index[0], y=max_index[1]+1))
                if(self.board[max_index[0]+1][max_index[1]]!=-1):
                    possibleActions.append(Action(player=self.pointer, x=max_index[0]+1, y=max_index[1]))
                if(self.board[max_index[0]-1][max_index[1]]!=-1):
                    possibleActions.append(Action(player=self.pointer, x=max_index[0]-1, y=max_index[1]))

        return possibleActions


    def takeAction(self, action):
        newState = deepcopy(self)
        newState.board[action.x][action.y] = action.player
        newState.pointer = self.pointer +1
        return newState

    def isTerminal(self):
        if(self.board[0][DIMENSION-1] !=0):
            return True
        else:
            return False

    def getReward(self):
        return 1


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
    ui = UserInterface()
    searcher = mcts(timeLimit=1000)
    epochs = 100

    print("Initial Position")
    play.displayBoard(ui)

    #Start player at the starting position at the maze
    play.changePointer(1)
    play.changeBoard(DIMENSION-1,0)

    for i in range(1,epochs-1):
        play.displayBoard(ui)
        try:
            #Update score on board as the current position of the player
            play.changePointer(i+1)
            action = searcher.search(initialState=play)
            print("Moving to",action)
            play.changeBoard(action.x,action.y)
        except Exception as e:
            if(play.isTerminal()):
                print("Destination Reached!")
            else:
                print("Could not reach destination")
            break


