#Donovan Rea's connect 4 CS130 assignment
#Run python file and play!

class GameBoard:
    def __init__(self, size):
        self.size = size
        self.num_entries = [0] * size
        self.items = [[0] * size for i in range(size)]
        self.points = [0] * 2

    def num_free_positions_in_column(self,column):
        if column >= 0 & column <= (self.size-1):
            free_pos = self.size - self.num_entries[column]
        
        return free_pos
    
    def game_over(self):
        free_pos = 0

        for i in range(0, self.size):
            if self.num_entries[i] != self.size:
                free_pos +=1
        
        #if the number of possible free positions left on the board is 0 then end the game
        if free_pos == 0:
            return True
        else:
            return False
                

    def display(self):
        size = self.size

        for i in range((size -1), -1, -1):
            for j in range(0, size, 1):
                if j == (size - 1):
                    #perimeter values
                    if self.items[i][j] == 2:
                        print('x ', end= '\n')
                    elif self.items[i][j] == 1:
                        print('o ', end= '\n')
                    elif self.items[i][j] == 0:
                        print('  ', end= '\n')

                else:
                    if self.items[i][j] == 2:
                        print('x ', end= '')
                    elif self.items[i][j] == 1:
                        print('o ', end= '')
                    elif self.items[i][j] == 0:
                        print('  ', end= '')
        
        
        print('-' * ((size * 2)-1))
            
        for i in range(size):
            if i == (size-1):
                print( str(i) , end = '\n')
            else:
                print( str(i) + ' ', end = '')

        print('Points player 1: {}' .format(self.points[0]))
        print('Points player 2: {}' .format(self.points[1]))
    
    def num_new_points(self,row,column,player):
        #compute the sum of all possible point-combinations from all directions for the given point
        return (self.horizontal_check(row,column,player)  + self.vertical_check(row,column,player) + self.right_diagonal_check(row,column,player) + self.left_diagonal_check(row,column,player))

    def horizontal_check(self,row,col,player):
        result = 0
        i = 0
        while i < 4:
            try:
                #check all surrounding combinations 
                if (self.items[row][col] == player  and self.items[row][col+1] == player  and self.items[row][col+2] == player  and self.items[row][col+3] == player):
                    result +=1        
                
                #if the point at the perimeter of the board then stop iterations
                if col == 0:
                    return result 

                col -= 1
            except IndexError:
                col -= 1

            i+=1
        
        return result


    def vertical_check(self,row,col,player):
        
        try:
            #check all surrounding combinations
            if (self.items[row][col] == player  and self.items[row-1][col] == player  and self.items[row-2][col] == player  and self.items[row-3][col] == player):
                return 1

        except IndexError:
            return 0 
        
        return 0

             
    def right_diagonal_check(self,row,col,player):
        result = 0
        i = 0
        while i < 4:
            try:
                #check all surrounding combinations
                if (self.items[row][col] == player  and self.items[row+1][col+1] == player  and self.items[row+2][col+2] == player  and self.items[row+3][col+3]== player):
                    result +=1
                col -= 1
                row -= 1
            except IndexError:
                row -= 1 
                col -= 1

            i+=1
        return result
    
    def left_diagonal_check(self,row,col,player):
        result = 0
        i = 0
        while i < 4:
            try:
                #check all surrounding combinations
                if (self.items[row][col] == player and  self.items[row-1][col+1] == player and self.items[row-2][col+2] == player and self.items[row-3][col+3] == player):
                    result +=1
                col -= 1
                row += 1
            except IndexError:
                col -= 1
                row += 1

            i+=1
        return result
       
 
    def add(self,column, player):
        if column < 0 and column >= (self.size):
            return False
        else:
            if self.num_free_positions_in_column(column) > 0:
                #compute the next row (depth) in which a token would land
                depth = (self.size-1)- (self.num_free_positions_in_column(column)-1)

                self.items[depth][column] = player
                self.num_entries[column] += 1
                self.points[player-1] += self.num_new_points(depth, column, player)

                return True
            else:
                return False
    
    def remove(self,column, player, points_to_remove):
        #remove function is only used as a helper for column_resulting_in_max_points function, removing points used for testing possible point options
        if column < 0 and column >= (self.size):
            return False
        else:
            
            depth = (self.size-1)- (self.num_free_positions_in_column(column))
            self.items[depth][column] = 0
            self.num_entries[column] -= 1
            self.points[player-1] -= points_to_remove

            return True
            

    
    def free_slots_as_close_to_middle_as_possible(self):
        
        num_slots_free = []
        #for cases where the board size is 1 
        if self.size == 1:
            if self.num_free_positions_in_column(0) != 0 :
                num_slots_free.append(0)
            
            return num_slots_free
        #for cases where the board size is 2
        elif self.size == 2:
            if self.num_free_positions_in_column(0) != 0 :
                num_slots_free.append(0)
            
            if self.num_free_positions_in_column(1) != 0 :
                num_slots_free.append(1)
            
            return num_slots_free
        #for cases where the board size is 3    
        elif self.size == 3:
            if self.num_free_positions_in_column(1) != 0 :
                num_slots_free.append(1)
            
            if self.num_free_positions_in_column(0) != 0 :
                num_slots_free.append(0)
            
            if self.num_free_positions_in_column(2) != 0 :
                num_slots_free.append(2)
            
            return num_slots_free
        #for all other cases where the board size> 3
        else:

            if (self.size) % 2 == 0:
                #initialise gap which mirrors the i counter so that list can be traversed up and down symultaneously 
                half = ((self.size-1)//2)
                gap = (half + 1)
            
                for i in range(half, -1, -1):
                    
                    if self.num_free_positions_in_column(i) != 0:
                        num_slots_free.append(i) 
                    if self.num_free_positions_in_column(gap) != 0:
                        num_slots_free.append(gap)
                    
                    gap += 1 
   
            else:
                half = int((self.size-1)/2)

                if self.num_entries[half] < ((self.size)-1):
                    num_slots_free.append(half)
                #initialise gap which mirrors the i counter so that list can be traversed up and down symultaneously 
                gap = (half +1)

                for i in range(half-1, -1, -1):
                    
                    if self.num_free_positions_in_column(i) != 0:
                        num_slots_free.append(i) 
                    if self.num_free_positions_in_column(gap) != 0:
                        num_slots_free.append(gap)
                    
                    gap += 1 

        return num_slots_free
    
    def column_resulting_in_max_points(self,player):
        next_availible_row_position = []
        col_sum_points = []
        col_sum_points_and_index = []

        #initialise array with the locations for where the next possible position in each row is 
        for i in self.num_entries:
            if i == self.size:
                next_availible_row_position.append(None)
            else:
                next_availible_row_position.append(i)

        #iterate through the columns; if the column isn't full then add token to obtain the number of points it would earn, then remove token
        for i in range(0,len(next_availible_row_position)):
            if next_availible_row_position[i] != None:

                self.add(i, player)
                new_possible_points = self.num_new_points(next_availible_row_position[i],i,player)
                self.remove(i, player, new_possible_points)
                col_sum_points.append(new_possible_points)
                col_sum_points_and_index.append([i, new_possible_points])
            
         
        free_spots_near_middle = self.free_slots_as_close_to_middle_as_possible()

        #if no possible options return nothing
        if len(col_sum_points) == 0:
            return 
        else:
            #find the max number of points and also find if there are any duplicates/ if the max number has duplicates
            max_points = col_sum_points[0]
            duplicates = []
            for i in range(1,len(col_sum_points)):
                if col_sum_points[i] > max_points:
                    max_points = col_sum_points[i] 
                elif (col_sum_points[i] == max_points) and (max_points != 0):
                    duplicates.append(col_sum_points[i])

            #if the max number is 0 then return the position closest to the middle
            if max_points == 0:
                return (free_spots_near_middle[0],0)
            elif (len(duplicates) > 0) and (max_points in duplicates): 
                #if the max is greater than 0 but it has duplicates then return the max closest to the middle 
                if max(duplicates) == max_points:
                    
                    for i in range(0, len(free_spots_near_middle)):
                        for j in range(0, len(col_sum_points_and_index)):
                            
                            if (free_spots_near_middle[i] == col_sum_points_and_index[j][0]) and (max_points == col_sum_points_and_index[j][1]):
                                return (col_sum_points_and_index[j][0], max_points)
                            
            else:
                #if the max has no duplicates then return the max & its location
                for i in col_sum_points_and_index:
                    if i[1] == max_points:
                        return(i[0], i[1])


class FourInARow:
    def __init__(self, size):
        self.board=GameBoard(size)
    def play(self):
        print("*****************NEW GAME*****************")
        self.board.display()
        player_number=0
        print()
        while not self.board.game_over():
            print("Player ",player_number+1,": ")
            if player_number==0:
                while True:
                    try:
                        column = int(input("Please input slot: "))       
                    except ValueError:
                        print("Input must be an integer in the range 0 to ", self.board.size)
                        continue
                    else:
                        if column<0 or column>=self.board.size:
                            print("Input must be an integer in the range 0 to ", self.board.size)
                            continue
                        else:
                            if self.board.add(column, player_number+1):
                                break
                            else:
                                print("Column ", column, "is alrady full. Please choose another one.")
                                continue
            else:
                # Choose move which maximises new points for computer player
                (c,maxPoints)=self.board.column_resulting_in_max_points(1)
                
                if maxPoints>0:
                    column=c
                else:
                    # if no move adds new points choose move which minimises points opponent player gets
                    (c,maxPoints)=self.board.column_resulting_in_max_points(2)
                    if maxPoints>0:
                        column=c
                    else:
                        # if no opponent move creates new points then choose column as close to middle as possible
                        column = self.board.free_slots_as_close_to_middle_as_possible()[0]
                self.board.add(column, player_number+1)
                print("The AI chooses column ", column)
            self.board.display()   
            player_number=(player_number+1)%2
        if (self.board.points[0]>self.board.points[1]):
            print("Player 1 (circles) wins!")
        elif (self.board.points[0]<self.board.points[1]):    
            print("Player 2 (crosses) wins!")
        else:  
            print("It's a draw!")
            
game = FourInARow(35)
game.play()    