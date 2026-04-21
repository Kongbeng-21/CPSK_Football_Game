import random


class Skin:
    """Represents a single player skin (head + leg images)."""

    def __init__(self, name, head_img, leg_img):
        self.name = name
        self.head_img = head_img
        self.leg_img = leg_img

    def __repr__(self):
        return f"Skin({self.name})"


class SkinManager:
    """Manages the player skins available in the game.

    Handles skin registration, random skin selection, per-player
    inventory management, and skin equipping.

    Attributes:
        available_skins  -- list of all registered Skin objects
        player_inventory -- dict mapping player id → list of owned Skin names
    """

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

    # ──────────────────────────────── Internal ───────────────────────────────

    def _register(self, skin: Skin):
        """Add a skin to the global available pool."""
        self.available_skins.append(skin)

    def _get_skin(self, name: str):
        for skin in self.available_skins:
            if skin.name == name:
                return skin
        return None

    # ──────────────────────────────── Public API ─────────────────────────────

    def random_skin(self) -> Skin:
        """Return a random skin from the available pool."""
        return random.choice(self.available_skins)

    def add_skin(self, player_id: str, skin_name: str):
        """Add a skin to a player's inventory (if not already owned)."""
        if skin_name not in self.player_inventory[player_id]:
            self.player_inventory[player_id].append(skin_name)

    def get_inventory(self, player_id: str):
        """Return list of Skin objects owned by a player."""
        return [
            self._get_skin(name)
            for name in self.player_inventory[player_id]
            if self._get_skin(name) is not None
        ]

    def equip_skin(self, player_id: str, skin_name: str):
        """Equip a skin for a player by name."""
        skin = self._get_skin(skin_name)
        if skin:
            self._equipped[player_id] = skin

    def get_equipped(self, player_id: str) -> Skin:
        """Return the currently equipped Skin for a player."""
        return self._equipped.get(player_id)
