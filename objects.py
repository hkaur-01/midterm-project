# objects.py

# Import dataclass to create a simple class with less code
from dataclasses import dataclass

# Import List, Dict, and Iterable for type hints
from typing import List, Dict, Iterable

# Tuple of valid baseball positions
# This is a constant and is used to validate player positions
POSITIONS = ("C", "1B", "2B", "3B", "SS", "LF", "CF", "RF", "P")


# Player class stores data for one baseball player
# @dataclass automatically creates the constructor and other useful methods
@dataclass
class Player:
    """Represents a single baseball player."""
    
    # Store player's first name
    first_name: str
    
    # Store player's last name
    last_name: str
    
    # Store player's playing position
    position: str
    
    # Store number of at bats
    at_bats: int
    
    # Store number of hits
    hits: int

    # Property to return full name by joining first and last name
    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    # Property to calculate batting average
    # If at_bats is 0, return 0.0 to avoid division by zero
    @property
    def average(self) -> float:
        """Batting average (0.0 if at_bats is 0)."""
        if self.at_bats == 0:
            return 0.0
        return self.hits / self.at_bats

    # Property to format batting average with 3 decimal places
    @property
    def average_str(self) -> str:
        """Average formatted with exactly 3 decimal places."""
        return f"{self.average:.3f}"


# Lineup class stores and manages multiple Player objects
class Lineup:
    """Holds the starting lineup and provides operations on it."""
    
    # Constructor creates an empty list of players
    def __init__(self) -> None:
        self._players: List[Player] = []

    # This allows us to loop through lineup using: for p in lineup
    def __iter__(self) -> Iterable[Player]:
        return iter(self._players)

    # This returns the number of players in the lineup
    def __len__(self) -> int:
        return len(self._players)

    # Add a new player object to the lineup
    def add_player(self, player: Player) -> None:
        self._players.append(player)

    # Return one player based on index
    def get_player(self, index: int) -> Player:
        return self._players[index]

    # Remove and return a player from the lineup using index
    def remove_player(self, index: int) -> Player:
        return self._players.pop(index)

    # Move a player from one position in the lineup to another
    def move_player(self, old_index: int, new_index: int) -> None:
        player = self._players.pop(old_index)
        self._players.insert(new_index, player)

    # Update the position of a player
    def update_position(self, index: int, new_position: str) -> None:
        self._players[index].position = new_position

    # Update the stats of a player
    def update_stats(self, index: int, at_bats: int, hits: int) -> None:
        self._players[index].at_bats = at_bats
        self._players[index].hits = hits


# ---------- Converters between dicts (for db) and objects ----------

# This function converts a list of dictionaries into a Lineup object
def lineup_from_dicts(player_dicts: List[Dict[str, object]]) -> Lineup:
    """Create a Lineup from a list of simple player dictionaries.

    Each dict has keys: name, position, at_bats, hits.
    """
    # Create an empty lineup
    lineup = Lineup()

    # Loop through each player dictionary
    for d in player_dicts:
        # Extract values from dictionary
        name = str(d["name"])
        position = str(d["position"])
        at_bats = int(d["at_bats"])
        hits = int(d["hits"])

        # Split full name into first name and last name
        # Example: "Tommy La Stella" becomes "Tommy" and "La Stella"
        parts = name.split(" ", 1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ""

        # Create a Player object
        player = Player(first_name, last_name, position, at_bats, hits)

        # Add player to lineup
        lineup.add_player(player)

    # Return the completed lineup
    return lineup


# This function converts a Lineup object back into a list of dictionaries
# This format is used when saving data back to the CSV file in db.py
def lineup_to_dicts(lineup: Lineup) -> List[Dict[str, object]]:
    """Convert a Lineup back into a list of dictionaries for db.py."""
    
    # Create an empty list to store dictionaries
    result: List[Dict[str, object]] = []

    # Loop through each player in the lineup
    for player in lineup:
        # Add player data as a dictionary
        result.append(
            {
                "name": player.full_name,
                "position": player.position,
                "at_bats": player.at_bats,
                "hits": player.hits,
            }
        )

    # Return the list of dictionaries
    return result