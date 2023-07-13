import random
from game import Board
import globals as globals

class Bot13521089(object):
    """
    Bot player
    """
    list_coord : list

    def __init__(self):
        self.player = None
        self.NIM = "13521089"
        self.center_cnt = 0
        self.list_coord = []

    def set_player_ind(self, p):
        self.player = p

    def get_action(self, board, return_var):

        try:
            location = self.get_input(board)
            if isinstance(location, str):  # for python3
                location = [int(n, 10) for n in location.split(",")]
            move = board.location_to_move(location)
        except Exception as e:
            move = -1

        while move == -1 or move not in board.availables:
            if globals.stop_threads:
                return
            try:
                location = self.get_input(board)
                if isinstance(location, str):  # for python3
                    location = [int(n, 10) for n in location.split(",")]
                move = board.location_to_move(location)
            except Exception as e:
                move = -1
        return_var.append(move) 

    def __str__(self):
        return "{} a.k.a Player {}".format(self.NIM,self.player)
    
    def get_input(self, board : Board) -> str:
        """
            Parameter board merepresentasikan papan permainan. Objek board memiliki beberapa
            atribut penting yang dapat menjadi acuan strategi.
            - board.height : int (x) -> panjang papan
            - board.width : int (y) -> lebar papan
            Koordinat 0,0 terletak pada kiri bawah

            [x,0] [x,1] [x,2] . . . [x,y]                               
            . . . . . . . . . . . . . . .  namun perlu diketahui        Contoh 4x4: 
            . . . . . . . . . . . . . . .  bahwa secara internal        11 12 13 14 15
            . . . . . . . . . . . . . . .  sel-sel disimpan dengan  =>  10 11 12 13 14
            [2,0] [2,1] [2,2] . . . [2,y]  barisan interger dimana      5  6  7  8  9
            [1,0] [1,1] [1,2] . . . [1,y]  kiri bawah adalah nol        0  1  2  3  4
            [0,0] [0,1] [0,2] . . . [0,y]          
                                 
            - board.states : dict -> Kondisi papan. 
            Key dari states adalah integer sel (0,1,..., x*y)
            Value adalah integer 1 atau 2:
            -> 1 artinya sudah diisi player 1
            -> 2 artinya sudah diisi player 2

            TODO: Tentukan x,y secara greedy. Kembalian adalah sebuah string "x,y"
        """


        # Greedy by weight
        # Weight Factors
        # Scale of 1-5
        # 1. Edge
        # 2. Number of the player's pawn
        # 3. Blocking rival's pawn if 3 in a row
        # 
        # If X and Y same, the weight will be combined linearly

        weight_1, x_1, y_1 = self.weight_center(board)
        weight_2, x_2, y_2 = self.weight_adj(board)

        if weight_2 > weight_1:
            x = x_2
            y = y_2
        else:
            x = x_1
            y = y_1
        self.list_coord.append([x,y])
        return f"{x},{y}"
    
    def to_coord(self, z, board):
        x = z // board.width
        y = z % board.width
        return x, y
    
    def to_number(self, x, y, board):
        return (board.width * x) + y
    
    def weight_center(self, board):
        weight = 0
        x = 0
        y = 0
        x_temp = board.height // 2
        y_temp = board.width // 2
        edges = [self.to_number(x_temp, y_temp, board), self.to_number(x_temp-1, y_temp-1, board), self.to_number(x_temp, y_temp-1, board), self.to_number(x_temp-1, y_temp, board)]

        for e in edges:
            if e in board.states:
                pass
            else:
                weight = 5 - self.center_cnt
                x, y = self.to_coord(e, board)
                self.center_cnt += 1
                break
    
        return weight, x, y
    
    def weight_adj(self, board):
        weight = 0
        x = 0
        y = 0
        best = 0
        
        rev = [4, 5, 6, 7, 0, 1, 2, 3]
        if len(self.list_coord) > 1:
            for i in reversed(self.list_coord):
                direction = [0 for i in range(8)]
                adj = [self.to_number(i[0]+1 % board.height, i[1] % board.width, board), 
                        self.to_number(i[0]+1 % board.height, i[1]+1 % board.width, board), 
                        self.to_number(i[0] % board.height, i[1]+1 % board.width, board), 
                        self.to_number(i[0]-1 % board.height, i[1]+1 % board.width, board), 
                        self.to_number(i[0]-1 % board.height, i[1] % board.width, board), 
                        self.to_number(i[0]-1 % board.height, i[1]-1 % board.width, board), 
                        self.to_number(i[0] % board.height, i[1]-1 % board.width, board), 
                        self.to_number(i[0]+1 % board.height, i[1]-1 % board.width, board)]
                for j in range(len(adj)):
                    if adj[j] in board.states and board.states[adj[j]] == self.player:
                        direction[j] -= 1
                        direction[rev[j]] += 1

                weight = max(direction)
                idx = direction.index(weight)
                if weight > best:
                    temp = [[1,0], [1,1], [0,1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]
                    best = weight
                    x = i[0] + temp[idx][0]
                    y = i[1] + temp[idx][1]

        return best + 2, x, y
    
    def weight_player(self, board):
        best = 0
        temp = [[0,0], 0]
        # Direction dimulai dari atas terus clockwise
        for i in self.list_coord:
            # Init direction
            direction = [0 for i in range(8)]
            # Pick a point
            curr = i
            # Recursion on the point
            point_coord, move, count = self.rec_get(direction, curr, board, -1)

            if count > best:
                temp = [point_coord, move]
                best = count
        
        adj = [[1,0], [1,1], [0,1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]
        x = temp[0][0] + adj[temp[1]][0]
        y = temp[0][1] + adj[temp[1]][1]
        return int(best + 5 - (len(self.list_coord))/5), x,y


    def rec_get(self, direction, point_coord, board, last_dir):
        adj = [self.to_number(point_coord[0]+1 % board.height, point_coord[1] % board.width, board), 
               self.to_number(point_coord[0]+1 % board.height, point_coord[1]+1 % board.width, board), 
               self.to_number(point_coord[0] % board.height, point_coord[1]+1 % board.width, board), 
               self.to_number(point_coord[0]-1 % board.height, point_coord[1]+1 % board.width, board), 
               self.to_number(point_coord[0]-1 % board.height, point_coord[1] % board.width, board), 
               self.to_number(point_coord[0]-1 % board.height, point_coord[1]-1 % board.width, board), 
               self.to_number(point_coord[0] % board.height, point_coord[1]-1 % board.width, board), 
               self.to_number(point_coord[0]+1 % board.height, point_coord[1]-1 % board.width, board)]
        max_idx = 0
        found = False
        rev = [4, 5, 6, 7, 0, 1, 2, 3]
        for j in range(len(adj)):
            if adj[j] in board.states:
                if board.states[adj[j]] == self.player and rev[j] != last_dir:
                    direction[j] += 1
                    found = True
                    max_idx = direction.index(max(direction))
        if found:
            return self.rec_get(direction, self.to_coord(adj[max_idx], board), board, max_idx)
        else:
            return point_coord, max_idx, direction[max_idx]
