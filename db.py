# db.py

from typing import List, Dict

FILENAME = "players.csv"


def read_players() -> List[Dict[str, object]]:
    """Read players from players.csv and return a list of dictionaries.

    Each dict has: name, position, at_bats, hits.
    Handles missing file by returning an empty list.
    """
    players: List[Dict[str, object]] = []

    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = [p.strip() for p in line.split(",")]
                if len(parts) != 4:
                    # Skip malformed lines
                    continue

                name, position, ab_str, hits_str = parts
                try:
                    at_bats = int(ab_str)
                    hits = int(hits_str)
                except ValueError:
                    # Skip lines with invalid numbers
                    continue

                players.append(
                    {
                        "name": name,
                        "position": position,
                        "at_bats": at_bats,
                        "hits": hits,
                    }
                )
    except FileNotFoundError:
        # Missing file -> start with empty lineup
        players = []

    return players


def write_players(players: List[Dict[str, object]]) -> None:
    """Write the given list of player dictionaries back to players.csv."""
    with open(FILENAME, "w", encoding="utf-8") as f:
        for p in players:
            line = f'{p["name"]},{p["position"]},{p["at_bats"]},{p["hits"]}\n'
            f.write(line)