from itertools import combinations

def solution(num_buns, num_required):
    bunnies = [[] for i in range(num_buns)]

    c = combinations(range(num_buns), num_buns - num_required + 1) 
    for index, bunny_combination in enumerate(c):
        for bunny_num in bunny_combination:
            bunnies[bunny_num].append(index)
    return bunnies

