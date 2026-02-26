# ui.py

from datetime import date, datetime
from typing import Optional, Callable

from objects import POSITIONS, Player, Lineup


# ---------- Generic input helpers ----------

def input_int(prompt: str) -> int:
    while True:
        raw = input(prompt)
        try:
            value = int(raw)
            return value
        except ValueError:
            print("Invalid integer. Please try again.")


def input_non_negative_int(prompt: str) -> int:
    while True:
        value = input_int(prompt)
        if value < 0:
            print("Value cannot be negative. Please try again.")
        else:
            return value


def input_position(prompt: str) -> str:
    while True:
        pos = input(prompt).upper()
        if pos in POSITIONS:
            return pos
        print(f"Invalid position. Valid positions: {', '.join(POSITIONS)}")


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


def get_menu_choice() -> int:
    while True:
        choice = input_int("Menu option: ")
        if 1 <= choice <= 7:
            return choice
        print("Invalid menu option. Please try again.")


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

    player = Player(first, last, position, at_bats, hits)
    lineup.add_player(player)
    print(f"{player.full_name} was added.")


def remove_player(lineup: Lineup) -> None:
    index = choose_lineup_index(lineup, "Number: ")
    if index is None:
        return
    player = lineup.remove_player(index)
    print(f"{player.full_name} was deleted.")


def move_player(lineup: Lineup) -> None:
    old_index = choose_lineup_index(lineup, "Current lineup number: ")
    if old_index is None:
        return
    player = lineup.get_player(old_index)
    print(f"{player.full_name} was selected.")
    new_index = choose_lineup_index(lineup, "New lineup number: ")
    if new_index is None:
        return
    lineup.move_player(old_index, new_index)
    print(f"{player.full_name} was moved.")


def edit_position(lineup: Lineup) -> None:
    index = choose_lineup_index(lineup)
    if index is None:
        return
    player = lineup.get_player(index)
    print(f"You selected {player.full_name} POS={player.position}")
    new_pos = input_position("Position: ")
    lineup.update_position(index, new_pos)
    print(f"{player.full_name} was updated.")


def edit_stats(lineup: Lineup) -> None:
    index = choose_lineup_index(lineup)
    if index is None:
        return
    player = lineup.get_player(index)
    print(
        f"You selected {player.full_name} AB={player.at_bats} H={player.hits}"
    )

    at_bats = input_non_negative_int("At bats: ")
    hits = input_non_negative_int("Hits: ")
    while hits > at_bats:
        print("Hits cannot be greater than at bats.")
        hits = input_non_negative_int("Hits: ")

    lineup.update_stats(index, at_bats, hits)
    print(f"{player.full_name} was updated.")


# ---------- Main UI loop ----------

def _save_with_error_handling(save_callback: Callable[[], None]) -> None:
    """Call save_callback, but catch file write errors and show message."""
    try:
        save_callback()
    except OSError as e:
        print(f"Error writing to players.csv: {e}")


def run(lineup: Lineup, save_callback: Callable[[], None]) -> None:
    game_date = get_game_date()

    while True:
        show_header(game_date)
        display_lineup(lineup)
        show_menu()
        choice = get_menu_choice()

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