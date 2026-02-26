# objects.py

from dataclasses import dataclass
from typing import List, Dict, Iterable

# Tuple of valid positions (rubric wants this as a constant)
POSITIONS = ("C", "1B", "2B", "3B", "SS", "LF", "CF", "RF", "P")


@dataclass
class Player:
    """Represents a single baseball player."""
    first_name: str
    last_name: str
    position: str
    at_bats: int
    hits: int

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()

    @property
    def average(self) -> float:
        """Batting average (0.0 if at_bats is 0)."""
        if self.at_bats == 0:
            return 0.0
        return self.hits / self.at_bats

    @property
    def average_str(self) -> str:
        """Average formatted with exactly 3 decimal places."""
        return f"{self.average:.3f}"


class Lineup:
    """Holds the starting lineup and provides operations on it."""
    def __init__(self) -> None:
        self._players: List[Player] = []

    # Iterator support: lets you do "for p in lineup"
    def __iter__(self) -> Iterable[Player]:
        return iter(self._players)

    def __len__(self) -> int:
        return len(self._players)

    # Core operations required by the spec
    def add_player(self, player: Player) -> None:
        self._players.append(player)

    def get_player(self, index: int) -> Player:
        return self._players[index]

    def remove_player(self, index: int) -> Player:
        return self._players.pop(index)

    def move_player(self, old_index: int, new_index: int) -> None:
        player = self._players.pop(old_index)
        self._players.insert(new_index, player)

    def update_position(self, index: int, new_position: str) -> None:
        self._players[index].position = new_position

    def update_stats(self, index: int, at_bats: int, hits: int) -> None:
        self._players[index].at_bats = at_bats
        self._players[index].hits = hits


# ---------- Converters between dicts (for db) and objects ----------

def lineup_from_dicts(player_dicts: List[Dict[str, object]]) -> Lineup:
    """Create a Lineup from a list of simple player dictionaries.

    Each dict has keys: name, position, at_bats, hits.
    """
    lineup = Lineup()
    for d in player_dicts:
        name = str(d["name"])
        position = str(d["position"])
        at_bats = int(d["at_bats"])
        hits = int(d["hits"])

        # Split "Tommy La Stella" -> "Tommy", "La Stella"
        parts = name.split(" ", 1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else ""

        player = Player(first_name, last_name, position, at_bats, hits)
        lineup.add_player(player)
    return lineup


def lineup_to_dicts(lineup: Lineup) -> List[Dict[str, object]]:
    """Convert a Lineup back into a list of dictionaries for db.py."""
    result: List[Dict[str, object]] = []
    for player in lineup:
        result.append(
            {
                "name": player.full_name,
                "position": player.position,
                "at_bats": player.at_bats,
                "hits": player.hits,
            }
        )
    return result