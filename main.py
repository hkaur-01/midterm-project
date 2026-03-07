# Import helper functions from objects.py
# lineup_from_dicts: converts raw dictionary data into a Lineup object
# lineup_to_dicts: converts the Lineup object back into dictionaries for saving
from objects import lineup_from_dicts, lineup_to_dicts

# Import db.py file to read and write CSV data
import db

# Import ui.py file to run the menu and user interaction
import ui


# Main function where the program starts
def main() -> None:
    # Step 1: Read all player records from the CSV file
    # The data comes as a list of dictionaries
    player_dicts = db.read_players()

    # Step 2: Convert the list of dictionaries into Player objects
    # and store them inside a Lineup object
    lineup = lineup_from_dicts(player_dicts)

    # Step 3: Create a save function
    # This function will be used whenever we want to save updated data
    def save() -> None:
        # Convert the current Lineup object back into dictionaries
        updated_dicts = lineup_to_dicts(lineup)

        # Write the updated dictionaries back into the CSV file
        db.write_players(updated_dicts)

    # Step 4: Start the user interface
    # This passes the lineup data and save function to ui.py
    ui.run(lineup, save)


# This makes sure the program runs only when this file is executed directly
# It prevents the code from running automatically if the file is imported somewhere else
if __name__ == "__main__":
    main()