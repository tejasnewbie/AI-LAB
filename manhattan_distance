goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

def manhattan_distance(tile, current_position, goal_position):
    current_x, current_y = current_position
    goal_x, goal_y = goal_position
    return abs(current_x - goal_x) + abs(current_y - goal_y)

def total_manhattan_distance(current_state):
    distance = 0
    for i in range(3):
        for j in range(3):
            tile = current_state[i][j]
            if tile != 0:
                goal_position = divmod(tile - 1, 3)
                distance += manhattan_distance(tile, (i, j), goal_position)
    return distance

states = [
    {
        'name': 'State 1',
        'state': [
            [1, 2, 3],
            [5, 4, 6],
            [7, 8, 0]
        ]
    },
    {
        'name': 'State 2 (One move from Goal)',
        'state': [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 0]
        ]
    },
    {
        'name': 'State 3 (Random positions)',
        'state': [
            [8, 1, 2],
            [4, 5, 3],
            [7, 6, 0]
        ]
    },
    {
        'name': 'State 4 (Completely scrambled)',
        'state': [
            [2, 8, 3],
            [1, 6, 4],
            [7, 0, 5]
        ]
    }
]

for state in states:
    distance = total_manhattan_distance(state['state'])
    print(f"{state['name']}:")
    for row in state['state']:
        print(row)
    print(f"Total Manhattan Distance: {distance}\n")
