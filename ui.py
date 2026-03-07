# ui.py

# Import date and datetime modules to work with current date and game date
from datetime import date, datetime

# Import Optional for values that can be None,
# and Callable for passing functions as arguments
from typing import Optional, Callable

# Import POSITIONS constant, Player class, and Lineup class from objects.py
from objects import POSITIONS, Player, Lineup


# ---------- Generic input helpers ----------

# This function takes integer input from the user
# It keeps asking until the user enters a valid integer
def input_int(prompt: str) -> int:
    while True:
        raw = input(prompt)
        try:
            value = int(raw)
            return value
        except ValueError:
            print("Invalid integer. Please try again.")


# This function makes sure the number entered is not negative
# It uses input_int() and checks if the value is 0 or more
def input_non_negative_int(prompt: str) -> int:
    while True:
        value = input_int(prompt)
        if value < 0:
            print("Value cannot be negative. Please try again.")
        else:
            return value


# This function asks the user to enter a baseball position
# It converts the input to uppercase and removes extra spaces
# Then it checks whether the position exists in the POSITIONS tuple
def input_position(prompt: str) -> str:
    while True:
        pos = input(prompt).upper().strip()
        if pos in POSITIONS:
            return pos
        print(f"Invalid position. Valid positions: {', '.join(POSITIONS)}")


# This function asks the user for the next game date
# The user must enter the date in YYYY-MM-DD format
# If the user presses Enter without typing anything, it returns None
def get_game_date() -> Optional[date]:
    """Ask user for game date in YYYY-MM-DD format or blank to skip."""
    while True:
        text = input("Enter next game date (YYYY-MM-DD) or press Enter to skip: ").strip()
        if text == "":
            return None
        try:
            return datetime.strptime(text, "%Y-%m-%d").date()
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")


# ---------- Display helpers ----------

# This function displays the program header
# It shows a title, today's date, and if available, the next game date
# It also calculates how many days are left until the game
def show_header(game_date: Optional[date]) -> None:
    print("=" * 64)
    print(" Baseball Team Manager ")
    print()

    today = date.today()
    print(f"CURRENT DATE: {today.isoformat()}")

    if game_date is not None:
        print(f"GAME DATE:    {game_date.isoformat()}")
        days = (game_date - today).days
        if days > 0:
            print(f"DAYS UNTIL GAME: {days}")
    print()


# This function displays all menu options for the user
# It also shows the list of valid baseball positions
def show_menu() -> None:
    print("MENU OPTIONS")
    print("1 – Display lineup")
    print("2 – Add player")
    print("3 – Remove player")
    print("4 – Move player")
    print("5 – Edit player position")
    print("6 – Edit player stats")
    print("7 – Exit program")
    print()
    print("POSITIONS")
    # Display positions by processing the tuple
    print(", ".join(POSITIONS))
    print("=" * 64)


# This function gets the user's menu choice
# It only accepts values from 1 to 7
def get_menu_choice() -> int:
    while True:
        choice = input_int("Menu option: ")
        if 1 <= choice <= 7:
            return choice
        print("Invalid menu option. Please try again.")


# This function displays the full lineup in table format
# It shows player number, full name, position, at bats, hits, and batting average
def display_lineup(lineup: Lineup) -> None:
    print()
    print(" Player                         POS   AB    H   AVG")
    print("-" * 64)
    for idx, player in enumerate(lineup, start=1):
        print(
            f"{idx:>2} {player.full_name:<28}"
            f"{player.position:<4}"
            f"{player.at_bats:>5}"
            f"{player.hits:>5}"
            f"{player.average_str:>6}"
        )
    print()


# ---------- Operations that modify the lineup ----------

# This function asks the user to choose a player number from the lineup
# It returns the index value in 0-based format
# If the lineup is empty, it returns None
def choose_lineup_index(lineup: Lineup, prompt: str = "Lineup number: ") -> Optional[int]:
    """Return 0-based index chosen by user, or None if lineup is empty."""
    if len(lineup) == 0:
        print("No players in the lineup.")
        return None

    while True:
        num = input_int(prompt)
        if 1 <= num <= len(lineup):
            return num - 1
        print("Invalid lineup number.")


# This function adds a new player to the lineup
# It asks for first name, last name, position, at bats, and hits
# It also makes sure hits are not greater than at bats
def add_player(lineup: Lineup) -> None:
    print()
    print("Add Player")
    first = input("First name: ")
    last = input("Last name: ")
    position = input_position("Position: ")
    at_bats = input_non_negative_int("At bats: ")
    hits = input_non_negative_int("Hits: ")

    while hits > at_bats:
        print("Hits cannot be greater than at bats.")
        hits = input_non_negative_int("Hits: ")

    # Create a Player object using the entered data
    player = Player(first, last, position, at_bats, hits)

    # Add the player to the lineup
    lineup.add_player(player)

    # Show confirmation message
    print(f"{player.full_name} was added.")


# This function removes a player from the lineup
# It first asks the user which player number to delete
def remove_player(lineup: Lineup) -> None:
    index = choose_lineup_index(lineup, "Number: ")
    if index is None:
        return

    # Remove player from lineup and store the removed player
    player = lineup.remove_player(index)

    # Show confirmation message
    print(f"{player.full_name} was deleted.")


# This function moves a player from one lineup position to another
def move_player(lineup: Lineup) -> None:
    old_index = choose_lineup_index(lineup, "Current lineup number: ")
    if old_index is None:
        return

    # Get the selected player from the current position
    player = lineup.get_player(old_index)
    print(f"{player.full_name} was selected.")

    # Ask for the new position in the lineup
    new_index = choose_lineup_index(lineup, "New lineup number: ")
    if new_index is None:
        return

    # Move the player to the new index
    lineup.move_player(old_index, new_index)
    print(f"{player.full_name} was moved.")


# This function updates a player's position
def edit_position(lineup: Lineup) -> None:
    index = choose_lineup_index(lineup)
    if index is None:
        return

    # Get the selected player
    player = lineup.get_player(index)
    print(f"You selected {player.full_name} POS={player.position}")

    # Ask for the new valid position
    new_pos = input_position("Position: ")

    # Update the player's position
    lineup.update_position(index, new_pos)
    print(f"{player.full_name} was updated.")


# This function updates a player's at bats and hits
def edit_stats(lineup: Lineup) -> None:
    index = choose_lineup_index(lineup)
    if index is None:
        return

    # Get the selected player
    player = lineup.get_player(index)
    print(
        f"You selected {player.full_name} AB={player.at_bats} H={player.hits}"
    )

    # Ask for new stats
    at_bats = input_non_negative_int("At bats: ")
    hits = input_non_negative_int("Hits: ")

    # Make sure hits are not greater than at bats
    while hits > at_bats:
        print("Hits cannot be greater than at bats.")
        hits = input_non_negative_int("Hits: ")

    # Update player stats
    lineup.update_stats(index, at_bats, hits)
    print(f"{player.full_name} was updated.")


# ---------- Main UI loop ----------

# This helper function tries to save the updated data
# If there is a file writing error, it shows an error message instead of crashing
def _save_with_error_handling(save_callback: Callable[[], None]) -> None:
    """Call save_callback, but catch file write errors and show message."""
    try:
        save_callback()
    except OSError as e:
        print(f"Error writing to players.csv: {e}")


# This is the main user interface loop of the program
# It keeps showing the menu until the user chooses to exit
def run(lineup: Lineup, save_callback: Callable[[], None]) -> None:
    # Ask user for game date at the beginning
    game_date = get_game_date()

    # Infinite loop until the user selects Exit
    while True:
        # Show heading with current date and game date
        show_header(game_date)

        # Display current lineup
        display_lineup(lineup)

        # Show menu options
        show_menu()

        # Get user's menu choice
        choice = get_menu_choice()

        # Perform action based on user's menu selection
        if choice == 1:
            display_lineup(lineup)
        elif choice == 2:
            add_player(lineup)
            _save_with_error_handling(save_callback)
        elif choice == 3:
            remove_player(lineup)
            _save_with_error_handling(save_callback)
        elif choice == 4:
            move_player(lineup)
            _save_with_error_handling(save_callback)
        elif choice == 5:
            edit_position(lineup)
            _save_with_error_handling(save_callback)
        elif choice == 6:
            edit_stats(lineup)
            _save_with_error_handling(save_callback)
        elif choice == 7:
            print("Bye!")
            break