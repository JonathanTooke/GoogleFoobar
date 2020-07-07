def solution(x, y):
    x,y = min(long(x), long(y)), max(long(x), long(y))
    cycles = 0
    while(True):
        if x < 1 or y < 1:
            return "impossible"
        if x == 1 or y == 1:
            return str(cycles + y - 1)
        reduce_factor = y/x
        y -= x*reduce_factor #subtract x from y y/x times
        cycles += reduce_factor #resulting in an additional y/x cycles
        x,y = y,x #swap x and y since y is now smaller than x
