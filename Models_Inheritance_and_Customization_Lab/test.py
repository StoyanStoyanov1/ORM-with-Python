def find_position(symbol, matrix):
    for row in range(len(matrix)):
        if symbol in matrix[row]:
            return [row, matrix[row].index(symbol)]


rows = int(input())

matrix = [[x for x in input()] for _ in range(rows)]

steps = {
    'up': [-1, 0],
    'down': [1, 0],
    'left': [0, -1],
    'right': [0, 1],
}

current_position = find_position("S", matrix)
catched_fish = 0
flag = True


while True:
    step = input()
    if step == "collect the nets":
        break

    current_row = current_position[0]
    current_col = current_position[1]

    matrix[current_row][current_col] = '-'

    next_row = current_row + steps[step][0]
    next_col = current_col + steps[step][1]

    if next_row not in range(len(matrix)):
        next_row = 0 if next_row >= len(matrix) else len(matrix) - 1
    elif next_col not in range(len(matrix[0])):
        next_col = 0 if next_col >= len(matrix[0]) else len(matrix[0]) - 1

    if matrix[next_row][next_col] == "W":
        flag = False
        print(f"You fell into a whirlpool! The ship sank and you lost the fish you caught."
              f"Last coordinates of the ship: [{next_row},{next_col}]")
        break

    elif matrix[next_row][next_col].isdigit():
        catched_fish += int(matrix[next_row][next_col])

    matrix[next_row][next_col] = "S"
    current_position = [next_row, next_col]

if flag:
    if catched_fish >= 20:
        print("Success! You managed to reach the quota!")

    else:
        print(f"You didn't catch enough fish and didn't reach the quota!You need {20 - catched_fish} tons of fish more.")

    if catched_fish > 0:
        print(f"Amount of fish caught: {catched_fish} tons.")

    [print(''.join(row)) for row in matrix]





