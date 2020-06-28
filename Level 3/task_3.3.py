#I later realised that dijkstra may have been a more efficient algorithm
#as this calculates all possible paths, but it is still in the same efficiency
#class as dikstra, running in polynomial time. 
def solution(m):
    maps = generate_maps(m)
    s_path = len(m) * len(m[0]) + 1
    for mapp in maps:
        s_path = min(s_path, mapp.shortest_path())
    return s_path

class Map:
    def __init__(self, m):
        """Constructor"""
        for i in range(len(m)):
            for j in range(len(m[i])):
                m[i][j] *= -1
        m[len(m)-1][len(m[0])-1] = 1
        self.num_rows, self.num_cols = len(m), len(m[0]) 
        self.current_row = len(m) - 1 #start on the last row
        self.m = m

    def shortest_path(self):
        """Calculate the shortest path from the bottom right to top left"""

        while self.current_row != 0:
            self.left_pass(self.current_row)
            self.right_pass(self.current_row)
            self.current_row -= 1
            self.left_pass(self.current_row)
            self.right_pass(self.current_row)
            self.current_row = self.down_pass(self.current_row)
            
    
        if self.m[0][0] == 0: #cannot reach the end with this map
            return self.num_rows*self.num_cols + 1 #return a path longer than the longest possible path

        return self.m[0][0] #return the calculated value               

    def left_pass(self, row_num):
        """Update the shortest path for each element in the row
        by taking the min of the element below and the element to the right"""
        for col in reversed(range(self.num_cols)):
            self.m[row_num][col] = self.lp_min(row_num, col)

    def lp_min(self, x, y):
        """At m[x][y] return the min of the current value, the value below, and the value to the right"""
        if self.m[x][y] == -1:
            return -1
        min_value, valid_entries = self.consider_elements(x+1,y,x,y+1) #consider value below, and to the right

        if valid_entries and self.m[x][y] == 0:
            return min_value + 1

        if not valid_entries:
            return self.m[x][y]

        return min(min_value + 1, self.m[x][y])
            
    def right_pass(self, row_num):
        """Update the shortest path for each element in the row
        by taking the min of the element below and the element to the left"""
        for col in range(self.num_cols):
            self.m[row_num][col] = self.rp_min(row_num, col)
    
    def rp_min(self, x, y):
        """At m[x][y] return the min of the current value, the value below, and the value to the left
        Note 0 and -1 not considered as min values"""
        if self.m[x][y] == -1:
            return -1
        
        min_value, valid_entries = self.consider_elements(x+1,y,x,y-1) #consider value below, and to the left

        if valid_entries and self.m[x][y] == 0:
            return min_value + 1

        if not valid_entries:
            return self.m[x][y]

        return min(min_value + 1, self.m[x][y])

    def down_pass(self, row_num):
        """Perform a downward pass for each element in the row. Return the 
        row number of the deepest row where a path length was updated"""
        deepest_row = row_num
        for col in range(self.num_cols):
            if self.m[row_num][col] not in [0,-1]:
                for row in range(row_num + 1, self.num_rows):
                    self.m[row][col], did_update = self.dp_min(row, col)
                    if not did_update:
                        deepest_row = max(row-1, deepest_row) #latest row to receive an update
                        break
                    if row == self.num_rows - 1:
                        deepest_row = self.num_rows - 1
        return deepest_row
                    
    def dp_min(self, x, y):
        """At m[x][y] return the min of the current value and the value above
        Note 0 and -1 not considered as min values
        Returns True if there was an update, False otherwise"""
    
        if self.m[x][y] > self.m[x-1][y] + 1 or self.m[x][y] == 0: #If a shorter path is found or the block has no current value --> update
            return self.m[x-1][y] + 1, True

        if self.m[x][y] <= self.m[x-1][y] + 1 or self.m[x][y] == -1 : #If the new path is longer or the block is a wall --> no update
            return self.m[x][y], False

    def consider_elements(self, x1, y1, x2, y2):
        """Returns the min of the valid entries m[x1][y1], m[x2][y2]
        An entry is not valid id it is a wall or it is out of bounds"""
        considering = []
        try:
            if x1 >= 0 and y1 >= 0: #python negative indexing
                considering.append(self.m[x1][y1])
        except IndexError:
            pass

        try:
            if x2 >= 0 and y2 >= 0: #python negative indexing
                considering.append(self.m[x2][y2])
        except IndexError:
            pass

        while -1 in considering:
            considering.remove(-1)
        
        while 0 in considering:
            considering.remove(0)

        if len(considering) > 0:
            return (reduce(lambda x,y: min(x,y), considering), True)

        return (-2, False) #if there are no valid elements
    
    def __str__(self):
        return '\n'.join([str(row) for row in self.m])
    
def generate_maps(m):
    """Generate a list of all of the possible maps by removing a different
    wall for each one"""
    maps = []
    for i in range(len(m)):
        for j in range(len(m[i])):
            if m[i][j] == 1:
                m[i][j] = 0 #remove wall
                maps.append(Map(copy_grid(m))) 
                m[i][j] = 1 #add wall back

    if len(maps) == 0:
        maps.append(Map(m)) #add the original map for the case that there are no walls

    return maps

def copy_grid(m):
    """Deep copy 2d list"""
    return [[elem for elem in row] for row in m]