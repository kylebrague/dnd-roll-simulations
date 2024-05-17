from character import Character

class Party:
    def __init__(self, characters: list[Character]):
        self.characters = characters
        self.all_downed_or_dead = self.get_all_downed_or_dead()

    def __len__(self):
        return len(self.characters)

    def count_not_dead_characters(self):
        return [not pc.is_dead for pc in self].count(True)

    def get_is_wiped(self):
        return all((pc.is_dead for pc in self))
    
    def get_all_downed_or_dead(self):
        return all((pc.is_downed or not pc.is_alive for pc in self))
    is_wiped: bool = property(get_is_wiped)

    def __iter__(self):
        return iter(self.characters)
