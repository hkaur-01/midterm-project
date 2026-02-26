import csv

FILENAME = "players.csv"

def read_players():
    """
    Reads players from players.csv.
    Returns a list of [name, position, at_bats, hits].
    """
    players = []
    try:
        with open(FILENAME, newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) != 4:
                    continue  # skip bad rows
                name = row[0]
                position = row[1]
                try:
                    at_bats = int(row[2])
                    hits = int(row[3])
                except ValueError:
                    # skip if numbers are bad
                    continue
                players.append([name, position, at_bats, hits])
    except FileNotFoundError:
        print("Could not find players.csv. Starting with empty lineup.")
    return players


def write_players(players):
    """
    Writes players back to players.csv.
    players: list of [name, position, at_bats, hits]
    """
    try:
        with open(FILENAME, "w", newline="") as file:
            writer = csv.writer(file)
            for player in players:
                writer.writerow(player)
    except OSError:
        print("Error writing to players.csv.")