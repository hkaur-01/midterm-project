# db.py

# Import List and Dict for type hints
from typing import List, Dict

# Constant variable that stores the CSV file name
FILENAME = "players.csv"


# This function reads player data from the CSV file
# and returns it as a list of dictionaries
def read_players() -> List[Dict[str, object]]:
    """Read players from players.csv and return a list of dictionaries.

    Each dict has: name, position, at_bats, hits.
    Handles missing file by returning an empty list.
    """
    
    # Create an empty list to store player records
    players: List[Dict[str, object]] = []

    try:
        # Open the CSV file in read mode
        with open(FILENAME, "r", encoding="utf-8") as f:
            
            # Read the file line by line
            for line in f:
                # Remove extra spaces and newline characters
                line = line.strip()

                # Skip empty lines
                if not line:
                    continue

                # Split the line by comma and remove extra spaces
                parts = [p.strip() for p in line.split(",")]

                # If the line does not have exactly 4 values, skip it
                if len(parts) != 4:
                    # Skip malformed lines
                    continue

                # Store the separated values into variables
                name, position, ab_str, hits_str = parts

                try:
                    # Convert at_bats and hits into integers
                    at_bats = int(ab_str)
                    hits = int(hits_str)
                except ValueError:
                    # Skip lines with invalid numbers
                    continue

                # Add player data as a dictionary into the list
                players.append(
                    {
                        "name": name,
                        "position": position,
                        "at_bats": at_bats,
                        "hits": hits,
                    }
                )

    except FileNotFoundError:
        # If the file does not exist, return an empty list
        # This allows the program to start with no players
        players = []

    # Return the final list of player dictionaries
    return players


# This function writes player data back into the CSV file
def write_players(players: List[Dict[str, object]]) -> None:
    """Write the given list of player dictionaries back to players.csv."""
    
    # Open the CSV file in write mode
    # This will overwrite the old file data with updated data
    with open(FILENAME, "w", encoding="utf-8") as f:
        
        # Loop through each player dictionary
        for p in players:
            
            # Convert dictionary values into CSV line format
            line = f'{p["name"]},{p["position"]},{p["at_bats"]},{p["hits"]}\n'
            
            # Write the line into the file
            f.write(line)