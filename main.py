
from copy import deepcopy
from algorithm.mcts import mcts
from algorithm.utils import randomBoard
from functools import reduce
import operator

DIMENSION = 3

class mazeEnvironmentState():
    def __init__(self):
        self.board = randomBoard(DIMENSION)
        self.currentPlayer = 1

    def changeCurrentPlayer(self,player):
        self.currentPlayer = player

    def changeBoard(self,x,y):
        newState = deepcopy(self)
        newState.board[x][y] = self.currentPlayer
        self.board = newState.board

    def displayBoard(self):
        print(self.board)

    def getCurrentPlayer(self):
        return self.currentPlayer

    def getPossibleActions(self):
        possibleActions = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j] == 0:
                    possibleActions.append(Action(player=self.currentPlayer, x=i, y=j))
        return possibleActions

    def takeAction(self, action):
        newState = deepcopy(self)
        newState.board[action.x][action.y] = action.player
        newState.currentPlayer = self.currentPlayer * -1
        return newState

    def isTerminal(self):
        for row in self.board:
            if abs(sum(row)) == DIMENSION:
                return True
        for column in list(map(list, zip(*self.board))):
            if abs(sum(column)) == DIMENSION:
                return True
        for diagonal in [[self.board[i][i] for i in range(len(self.board))],
                         [self.board[i][len(self.board) - i - 1] for i in range(len(self.board))]]:
            if abs(sum(diagonal)) == DIMENSION:
                return True
        return reduce(operator.mul, sum(self.board, []), 1)

    def getReward(self):
        for row in self.board:
            if abs(sum(row)) == DIMENSION:
                return sum(row) / DIMENSION
        for column in list(map(list, zip(*self.board))):
            if abs(sum(column)) == DIMENSION:
                return sum(column) / DIMENSION
        for diagonal in [[self.board[i][i] for i in range(len(self.board))],
                         [self.board[i][len(self.board) - i - 1] for i in range(len(self.board))]]:
            if abs(sum(diagonal)) == DIMENSION:
                return sum(diagonal) / DIMENSION
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
    epochs = 10

    for i in range(epochs):
        if(i%2==0):
            play.changeCurrentPlayer(1)
        else:
            play.changeCurrentPlayer(2)
        play.displayBoard()
        try:
            action = searcher.search(initialState=play)
            print(action)
            play.changeBoard(action.x,action.y)
        except Exception as e:
            print("Game Ended!")
            break


