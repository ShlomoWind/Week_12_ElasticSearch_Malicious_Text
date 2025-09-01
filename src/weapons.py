class Weapon:
    def __init__(self,fie_path,text):
        self.text = text
        with open(fie_path, "r") as f:
            self.weapons = [line.strip() for line in f.readlines()]

    def weapon_blacklist(self):
        found_weapons = [weapon for weapon in self.weapons if weapon in self.text]
        return found_weapons if found_weapons else None