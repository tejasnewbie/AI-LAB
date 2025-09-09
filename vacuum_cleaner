class VacuumCleaner:
    def __init__(self):
        self.location = 'A'
        self.room = {'A': 'dirty', 'B': 'clean'}

    def clean(self):
        print(f"Location A is {self.room['A']}, Location B is {self.room['B']}")
        if self.room[self.location] == 'dirty':
            print(f"Cleaning {self.location}...")
            self.room[self.location] = 'clean'
        if self.location == 'A':
            self.location = 'B'
        else:
            self.location = 'A'
        print(f"Moved to {self.location}")
    
    def is_clean(self):
        return self.room['A'] == 'clean' and self.room['B'] == 'clean'

vacuum = VacuumCleaner()

while not vacuum.is_clean():
    vacuum.clean()

print("Both rooms are clean!")
