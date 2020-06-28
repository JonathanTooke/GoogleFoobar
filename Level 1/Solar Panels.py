def solution(area):
    squares = [i**2 for i in range(1001)]
    answer = []

    while(area != 0):
        for i in range(len(squares)):
            if (squares[i] == area):
                answer.append(squares[i])
                return answer
            elif (squares[i] > area):
                answer.append(squares[i - 1])
                area -= squares[i - 1]
                break

    return answer