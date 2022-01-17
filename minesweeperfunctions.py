#create board and randomize bomb spots
#prompt where to dig first
#if location is where bomb is, then gg
#if location is safe, dig recursively until every square is at lesat next to a bomb
#repeat until there are no more places to dig -> W secured
import random
import re

class Board:
    def __init__(self, dimensions, num_bombs):
        self.dimensions = dimensions
        self.num_bombs = num_bombs

        #create the board
        self.board = self.make_new_board() #plant bombs
        self.assign_values_to_board()

        #initialize a set to keep track of which locations we've uncovered
        #saved as (row, col) tuple 
        self.areas_dug = set() #if we dig at 0,0 then self.areas_dug = {(0,0)}

    def make_new_board(self):
        #make new board based on dimensions and num bombs
        #we should construct the list of lists here 
        board = [[None for _ in range(self.dimensions)] for _ in range(self.dimensions)]
        #generates an array that looks like:
        #[[None, None, ... , None]
        # [None, None, ... , None]
        # [None, None, ... , None]
        # [None, None, ... , None]]
        planted_bombs = 0
        while planted_bombs < self.num_bombs:
            location = random.randint(0, self.dimensions**2-1)
            row = location // self.dimensions
            col = location % self.dimensions

            if board[row][col] == '*':
                #this means we've actually planted a bomb there already
                continue

            board[row][col] = '*'
            planted_bombs+=1
        return board

    def assign_values_to_board(self):
        for r in range(self.dimensions):
            for c in range(self.dimensions):
                if self.board[r][c] == '*':
                    continue
                self.board[r][c] = self.get_num_neighbouring_bomb(r, c)

    def get_num_neighbouring_bomb(self, row, column):
        #(row-1, col-1) | (row-1, col) | (row-1, col+1)
        #(row, col-1) | X | (row, col+1)
        #(row+1, col-1) | (row+1, col) | (row+1, col+1)
        number_neighbour_bomb =0
        for r in range(max(0,row-1), min(self.dimensions-1, row+1)+1):
            for c in range(max(0, column-1), min(self.dimensions-1, column+1)+1):
                if r == row and c==column:
                    continue
                elif self.board[r][c]=="*":
                    number_neighbour_bomb+=1
        return number_neighbour_bomb
    
    def dig_operation(self, row, col):
        #dig at location user specifies
        #return Treu if successful dig, False if bomb is dug

        self.areas_dug.add((row, col)) #keep track that we dug here
        if self.board[row][col] == "*": 
            return False
        elif self.board[row][col] > 0: 
            return True

        #when self.board[row][col]==0
        for r in range(max(0, row-1), min(self.dimensions-1, row+1)+1):
            for c in range(max(0, col-1), min(self.dimensions-1, col+1)+1):
                if(r,c) in self.areas_dug: continue
                self.dig_operation(r,c)
        return True
    
    def __str__(self):
        #functino where if you call print on the object, it'll print out what the function returns
        visible_board = [[None for _ in range(self.dimensions)] for _ in range(self.dimensions)]
        for row in range(self.dimensions):
            for col in range(self.dimensions):
                if(row,col) in self.areas_dug: 
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    visible_board[row][col] = ' '
        
        # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dimensions):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(len(max(columns, key = len)))

    # print the csv strings
        indices = [i for i in range(self.dimensions)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dimensions)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep


def play(dimensions, num_bombs):
    #create board and plant bombs
    board = Board(dimensions, num_bombs)

    valid_dig = True
    while len(board.areas_dug) < board.dimensions**2 - num_bombs:
        print(board) 
        user_guess = re.split(',(\\s)*', input("enter the coordinates of where you want to guess: "))
        row, col = int(user_guess[0]), int(user_guess[-1])
        if row<0 or row>=board.dimensions or col<0 or col>=dimensions:
            print("not a valid input, enter again: ")
            continue

        valid_dig = board.dig_operation(row, col)
        if not valid_dig: #bomb dug
            break
    
    if valid_dig:
        print("yay you win")
    else:
        print("you lose")
        board.areas_dug = [(r,c) for r in range(board.dimensions) for c in range(board.dimensions)]
        print(board)