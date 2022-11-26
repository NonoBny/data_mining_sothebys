class Artist:
    def __init__(self, name, life, bio):
        self.name = name
        self.life = life
        self.bio = bio

    def print(self):
        print(f'Artist Name: {str(self.name)}\n+Life: {str(self.life)}\n+ Biography {str(self.bio)}')



