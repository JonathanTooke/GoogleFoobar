processed_nodes = []

def solution(src, dest):
    unprocessed_nodes = [src]
    count = 0
    
    while len(unprocessed_nodes) > 0:
        if dest in unprocessed_nodes:
            return count

        new_nodes = []
        for node in unprocessed_nodes:
            new_nodes.extend(get_adjacent_nodes(node))

        processed_nodes.extend(unprocessed_nodes)    
        unprocessed_nodes = new_nodes

        count += 1
            
def get_adjacent_nodes(number):
    x, y = map_number_to_index(number)
    adjacent_nodes = []
    if is_valid(x+1, y-2): #up 2, right 1
        adjacent_nodes.append(map_index_to_number(x+1, y-2))
    
    if is_valid(x+1, y+2): #down 2, right 1
        adjacent_nodes.append(map_index_to_number(x+1, y+2))
    
    if is_valid(x+2, y+1): #right 2, down 1 
        adjacent_nodes.append(map_index_to_number(x+2, y+1))
    
    if is_valid(x+2, y-1): #right 2, up 1
        adjacent_nodes.append(map_index_to_number(x+2, y-1))

    if is_valid(x-2, y+1): #left 2, down 1
        adjacent_nodes.append(map_index_to_number(x-2, y+1))

    if is_valid(x-2, y-1): #left 2, up 1
        adjacent_nodes.append(map_index_to_number(x-2, y-1))

    if is_valid(x-1, y-2): #up 2, left 1
        adjacent_nodes.append(map_index_to_number(x-1, y-2))
    
    if is_valid(x-1, y+2): #down 2, left 1
        adjacent_nodes.append(map_index_to_number(x-1, y+2))

    for node in adjacent_nodes:
        if node in processed_nodes:
            adjacent_nodes.remove(node)
        
    return adjacent_nodes

def is_valid(x, y):
    if x < 0 or x > 7 or y < 0 or y > 7:
        return False
    return True

def map_number_to_index(number):
    x = number % 8
    y = number // 8
    return (x, y)

def map_index_to_number(x, y):
    return y*8 + x