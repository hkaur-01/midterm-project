from db import read_players, write_players

# Valid positions tuple (as required)
VALID_POSITIONS = ("C", "1B", "2B", "3B", "SS", "LF", "CF", "RF", "P")


def display_title():
    print("=" * 64)
    print(" Baseball Team Manager")
    print("=" * 64)
    print("POSITIONS")
    print(", ".join(VALID_POSITIONS))
    print("=" * 64)


def display_menu():
    print("\nMENU OPTIONS")
    print("1 – Display lineup")
    print("2 – Add player")
    print("3 – Remove player")
    print("4 – Move player")
    print("5 – Edit player position")
    print("6 – Edit player stats")
    print("7 – Exit program")


def get_int(prompt):
    """Ask for an int and handle invalid input."""
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Invalid integer. Please try again.")


def calc_average(at_bats, hits):
    """Return batting average, rounded to 3 decimals. 0.0 if at_bats is 0."""
    if at_bats == 0:
        return 0.0
    return round(hits / at_bats, 3)


def display_lineup(players):
    """Show the lineup table."""
    if not players:
        print("No players in lineup.")
        return

    print("\n {:<3} {:<20} {:<3} {:>5} {:>3} {:>6}".format(
        "#", "Player", "POS", "AB", "H", "AVG"))
    print("-" * 64)

    for i, player in enumerate(players, start=1):
        name, pos, ab, hits = player
        avg = calc_average(ab, hits)
        print(" {:<3} {:<20} {:<3} {:>5} {:>3} {:>6.3f}".format(
            i, name, pos, ab, hits, avg))


def get_valid_position():
    """Ask until user enters a valid baseball position."""
    while True:
        pos = input("Position: ").upper().strip()
        if pos in VALID_POSITIONS:
            return pos
        else:
            print("Invalid position. Valid positions are:")
            print(", ".join(VALID_POSITIONS))


def add_player(players):
    print("\nADD PLAYER")
    name = input("Name: ").strip()
    position = get_valid_position()

    at_bats = get_int("At bats: ")
    while at_bats < 0:
        print("At bats cannot be negative.")
        at_bats = get_int("At bats: ")

    hits = get_int("Hits: ")
    while hits < 0 or hits > at_bats:
        print("Hits must be between 0 and at bats.")
        hits = get_int("Hits: ")

    players.append([name, position, at_bats, hits])
    print(f"{name} was added.")


def remove_player(players):
    print("\nREMOVE PLAYER")
    display_lineup(players)
    number = get_int("Number: ")

    if number < 1 or number > len(players):
        print("Invalid player number.")
        return

    removed = players.pop(number - 1)
    print(f"{removed[0]} was deleted.")


def move_player(players):
    print("\nMOVE PLAYER")
    display_lineup(players)

    current = get_int("Current lineup number: ")
    if current < 1 or current > len(players):
        print("Invalid player number.")
        return

    player = players.pop(current - 1)
    print(f"{player[0]} was selected.")

    new = get_int("New lineup number: ")
    if new < 1 or new > len(players) + 1:
        print("Invalid new position.")
        # put player back in original place
        players.insert(current - 1, player)
        return

    players.insert(new - 1, player)
    print(f"{player[0]} was moved.")


def edit_position(players):
    print("\nEDIT PLAYER POSITION")
    display_lineup(players)

    number = get_int("Lineup number: ")
    if number < 1 or number > len(players):
        print("Invalid player number.")
        return

    player = players[number - 1]
    print(f"You selected {player[0]} POS={player[1]}")

    new_pos = get_valid_position()
    player[1] = new_pos
    print(f"{player[0]} was updated.")


def edit_stats(players):
    print("\nEDIT PLAYER STATS")
    display_lineup(players)

    number = get_int("Lineup number: ")
    if number < 1 or number > len(players):
        print("Invalid player number.")
        return

    player = players[number - 1]
    print(f"You selected {player[0]} AB={player[2]} H={player[3]}")

    at_bats = get_int("New at bats: ")
    while at_bats < 0:
        print("At bats cannot be negative.")
        at_bats = get_int("New at bats: ")

    hits = get_int("New hits: ")
    while hits < 0 or hits > at_bats:
        print("Hits must be between 0 and at bats.")
        hits = get_int("New hits: ")

    player[2] = at_bats
    player[3] = hits
    print(f"{player[0]} was updated.")


def main():
    players = read_players()   # load from CSV
    display_title()

    while True:
        display_menu()
        option = get_int("Menu option: ")

        if option == 1:
            display_lineup(players)
        elif option == 2:
            add_player(players)
        elif option == 3:
            remove_player(players)
        elif option == 4:
            move_player(players)
        elif option == 5:
            edit_position(players)
        elif option == 6:
            edit_stats(players)
        elif option == 7:
            write_players(players)   # save to CSV
            print("Bye!")
            break
        else:
            print("Invalid menu option. Please try again.")


if __name__ == "__main__":
    main()