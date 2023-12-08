def find_position(symbol, matrix):
    for row in range(len(matrix)):
        if symbol in matrix[row]:
            return (row, matrix[row].index(symbol))


def out_of_matrix(len_matrix, index):
    return len_matrix if index < 0 else 0


rows = int(input())

matrix = [[x for x in input()] for _ in range(rows)]
my_positions_indexes = find_position("S", matrix)

directions = {
    "up": (-1, 0),
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1)
}

tons = 0
fell_into_whirlpool = False

while True:
    command = input()
    if command == "collect the nets":
        break

    current_row = my_positions_indexes[0]
    current_col = my_positions_indexes[1]

    matrix[current_row][current_col] = '-'

    current_row += directions[command][0]
    current_col += directions[command][1]

    if current_row not in range(len(matrix)):
        current_row = out_of_matrix(len(matrix) - 1, current_row)
    if current_col not in range(len(matrix[0])):
        current_col = out_of_matrix(len(matrix[0]) - 1, current_col)

    current_symbol_position = matrix[current_row][current_col]
    if current_symbol_position == "W":
        print(f"You fell into a whirlpool! "
              f"The ship sank and you lost the fish you caught. "
              f"Last coordinates of the ship: [{current_row},{current_col}]")
        fell_into_whirlpool = True
        break

    elif current_symbol_position.isdigit():
        tons += int(current_symbol_position)

    matrix[current_row][current_col] = "S"
    my_positions_indexes = (current_row, current_col)

if not fell_into_whirlpool:
    if tons >= 20:
        print("Success! You managed to reach the quota!")
    else:
        print(f"You didn't catch enough fish and didn't reach the quota! You need {20 - tons} tons of fish more.")

    if tons:
        print(f"Amount of fish caught: {tons} tons.")

    [print(''.join(x)) for x in matrix]
