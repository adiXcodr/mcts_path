from tkinter import *
import time
  
class UserInterface:
    def __init__(self):
        self.root = Tk()
        self.e = None

    def run_loop(self):
        while True:
            self.root.update_idletasks()
            self.root.update()
            time.sleep(2)
            self.root.quit()
            break

    def display_table(self,board):
        rows = cols = len(board)
        for i in range(rows):
            for j in range(cols):
                  
                self.e = Entry(self.root, width=20, fg='blue',
                               font=('Arial',16,'bold'))
                  
                self.e.grid(row=i, column=j)
                self.e.insert(END, board[i][j])

    def close_window(self):
        self.root.destroy()
