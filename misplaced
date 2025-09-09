goal_state = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

def misplaced_tiles(current_state):
    misplaced = 0
    for i in range(3):
        for j in range(3):
            tile = current_state[i][j]
            if tile != 0 and tile != goal_state[i][j]:
                misplaced += 1
    return misplaced

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
    misplaced = misplaced_tiles(state['state'])
    print(f"{state['name']}:")
    for row in state['state']:
        print(row)
    print(f"Misplaced Tiles: {misplaced}\n")
