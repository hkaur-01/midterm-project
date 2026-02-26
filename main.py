# main.py

from objects import lineup_from_dicts, lineup_to_dicts
import db
import ui


def main() -> None:
    # 1. Read raw player data (list of dictionaries) from CSV
    player_dicts = db.read_players()

    # 2. Convert dictionaries into Player objects inside a Lineup
    lineup = lineup_from_dicts(player_dicts)

    # 3. Define how to save the current lineup back to the CSV
    def save() -> None:
        updated_dicts = lineup_to_dicts(lineup)
        db.write_players(updated_dicts)

    # 4. Hand control to the UI
    ui.run(lineup, save)


if __name__ == "__main__":
    main()