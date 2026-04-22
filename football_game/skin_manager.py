import random

class Skin:
    def __init__(self, name, head_img, leg_img):
        self.name = name
        self.head_img = head_img
        self.leg_img = leg_img
        

    def __repr__(self):
        return f"Skin({self.name})"


class SkinManager:
    def __init__(self, ske_head, ske_leg, cpe_head, cpe_leg):
        self.available_skins = []
        self.player_inventory = {
            "p1": [],
            "p2": [],
        }
        self._equipped = {
            "p1": None,
            "p2": None,
        }

        # Register built-in skins
        self._register(Skin("SKE", ske_head, ske_leg))
        self._register(Skin("CPE", cpe_head, cpe_leg))

        # Default loadout
        self.equip_skin("p1", "SKE")
        self.equip_skin("p2", "CPE")

        # Give both players all available skins by default
        for skin in self.available_skins:
            self.add_skin("p1", skin.name)
            self.add_skin("p2", skin.name)

    def _register(self, skin: Skin):
        """Add a skin to the global available pool."""
        self.available_skins.append(skin)

    def _get_skin(self, name: str):
        for skin in self.available_skins:
            if skin.name == name:
                return skin
        return None


    def random_skin(self) -> Skin:
        return random.choice(self.available_skins)

    def add_skin(self, player_id: str, skin_name: str):
        if skin_name not in self.player_inventory[player_id]:
            self.player_inventory[player_id].append(skin_name)

    def get_inventory(self, player_id: str):
        return [
            self._get_skin(name)
            for name in self.player_inventory[player_id]
            if self._get_skin(name) is not None
        ]

    def equip_skin(self, player_id: str, skin_name: str):
        skin = self._get_skin(skin_name)
        if skin:
            self._equipped[player_id] = skin

    def get_equipped(self, player_id: str) -> Skin:
        return self._equipped.get(player_id)
