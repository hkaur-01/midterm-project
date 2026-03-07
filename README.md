# Baseball Team Manager – CPRO 2201 Midterm Project

## Project Overview

This project implements a **Baseball Team Manager** console application using Python.

The program allows a user to manage a baseball lineup by displaying players, adding players, removing players, moving players in the lineup, and editing player statistics.

This project demonstrates the following programming concepts:

 Object-Oriented Programming (OOP)
 File handling with CSV
 Modular program design
 Input validation and error handling

This project was developed as part of the **CPRO 2201 Python Programming II Midterm Project**.

---

## Features

The program provides the following menu options:

1. Display lineup
2. Add player
3. Remove player
4. Move player
5. Edit player position
6. Edit player stats
7. Exit program

Additional functionality includes:

* Batting average calculation
* Input validation
* Prevents hits from being greater than at-bats
* Automatically saves changes to the CSV file
* Displays the current date and optional game date

---

## Project Structure

| File          | Description                                                      |
| ------------- | ---------------------------------------------------------------- |
| `main.py`     | Entry point of the program. Loads player data and starts the UI. |
| `ui.py`       | Handles the menu system and all user interaction.                |
| `objects.py`  | Contains the `Player` and `Lineup` classes.                      |
| `db.py`       | Handles reading and writing player data to the CSV file.         |
| `players.csv` | Stores player data (name, position, at-bats, hits).              |

---

## How to Run the Program

1. Make sure **Python 3** is installed.

2. Clone the repository:

```bash
git clone https://github.com/hkaur-01/midterm-project.git
```

3. Navigate to the project folder:

```bash
cd midterm-project
```

4. Run the program:

```bash
python main.py
```

---

## CSV File Format

The `players.csv` file must follow this format:

```
FirstName LastName,Position,AtBats,Hits
```

Example:

```
Buster Posey,C,4575,1380
Brandon Crawford,SS,4200,1185
Mike Yastrzemski,RF,1600,410
```

---

## Valid Positions

The program only accepts the following baseball positions:

```
C, 1B, 2B, 3B, SS, LF, CF, RF, P
```

---

## Video Demonstration

A video explanation of the project, including code walkthrough and program demonstration, is available here:

**YouTube Link:** *(https://youtu.be/oMGWMEjM8lw)

---

## Author

Harpreet Kaur


