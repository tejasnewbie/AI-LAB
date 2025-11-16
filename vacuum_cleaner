# Initial state
location = 'A'
room = {'A': 'dirty', 'B': 'clean'}

def print_status():
    print(f"Location A is {room['A']}, Location B is {room['B']}")

def clean_room():
    global location

    print_status()

    # If current location is dirty → clean it
    if room[location] == 'dirty':
        print(f"Cleaning {location}...")
        room[location] = 'clean'

    # Move to the other room
    if location == 'A':
        location = 'B'
    else:
        location = 'A'

    print(f"Moved to {location}")

def is_clean():
    return room['A'] == 'clean' and room['B'] == 'clean'


# Main loop
while not is_clean():
    clean_room()

print("Both rooms are clean!")
