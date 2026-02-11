from game_logic import feedback
from data import wordlist
import heuristics as h

import tkinter as tk
import random

answer = random.choice(wordlist)

current_row = 0
simulation_target = 0
simulation_count = 0
current_start_word = None
stats = {}

def submit_guess():
    global current_row

    guess = "".join(cells[current_row][col].get().upper() for col in range (Columns))

    if len(guess) != Columns or not guess.isalpha():
        print("Incomplete or invalid guess")
        return
    
    if guess == answer:
        print("WIN", guess)
        end_game(win=True)
        return "win"
    
    if current_row == Rows -1:
        print("LOSE", answer)
        end_game(win=False)
        return "loss"

    colors = feedback(guess, answer)

    for col in range(Columns):
        cells[current_row][col].config(bg=colors[col])

    current_row += 1
    return False

def end_game(win):
    if win:
        print("You guessed correctly")
    else:
        print("Out of guesses")
    reset_game()

def reset_game():
    global current_row, answer
    current_row = 0

    # Clear all cells
    for r in range(Rows):
        for c in range(Columns):
            cells[r][c].delete(0, tk.END)
            cells[r][c].config(bg="white")

    # Pick a new word
    answer = random.choice(wordlist)
    answer_label.config(text=f"Correct word (debug): {answer}")


def validate_input(new_value, char):
    if char.isdigit():
        return False
    
    if len(new_value) > 1:
        return False
    return True

Rows, Columns = 6,5
root = tk.Tk()
root.title("Wordies, a legally distinct version from the game of Wordle")

cells = [[None for _ in range(Columns)] for _ in range(Rows)]

vcmd = (root.register(validate_input), "%P", "%S")

for row in range(Rows):
    for col in range(Columns):
        entry = tk.Entry(
            root,
            width=2,
            justify="center",
            font=("Arial", 14),
            validate = "key",
            validatecommand=vcmd
        )

        entry.grid(row=row, column=col, padx=2, pady=2)
        cells[row][col] = entry

answer_label = tk.Label(root, text=f"Correct word: {answer}", font=("Aerial", 12))
answer_label.grid(row=Rows +1, column=0, columnspan=Columns, pady=10)

def play_guess(guess):
    global current_row

    for col, letter in enumerate(guess):
        cells[current_row][col].delete(0, tk.END)
        cells[current_row][col].insert(0, letter)

    colors = feedback(guess, answer)

    for col in range(Columns):
        cells[current_row][col].config(bg=colors[col])

    if guess == answer:
        print("WIN", guess)
        end_game(win=True)
        return True
    
    if current_row == Rows-1:
        print("LOSE", answer)
        end_game(win=False)
        return True
    
    current_row += 1
    return False

def auto_play(strategy, start_word=None):
    candidates = wordlist.copy()
    first_move = True

    def step():
        nonlocal candidates, first_move
        global simulation_count

        # --- Choose guess ---
        if first_move and start_word is not None:
            guess = start_word
        else:
            guess = strategy(candidates)

        result = play_guess(guess)
        fb = feedback(guess, answer)

        # --- Track first-guess colors ---
        if first_move:
            for color in fb:
                if color == "green":
                    stats[current_start_word]["greens"] += 1
                elif color == "yellow":
                    stats[current_start_word]["yellows"] += 1
                else:
                    stats[current_start_word]["grays"] += 1
            first_move = False

        # --- Reduce candidates ---
        candidates = [w for w in candidates if feedback(guess, w) == fb]
        #print("Candidates left:", len(candidates))

        # --- Handle end-of-game ---
        if result in ("win", "loss"):
            stats[current_start_word]['games'] += 1
            if result == "win":
                stats[current_start_word]['wins'] += 1
            stats[current_start_word]['total_turns'] += current_row
            simulation_count += 1

            if simulation_count >= simulation_target:
                print("Finished simulations")
                print(stats[current_start_word])
                return

            reset_game()
            root.after(100, lambda: auto_play(strategy, current_start_word))
            return  # important!

        # --- Continue same game ---
        root.after(100, step)

    step()


def run_simulations(start_word, n_games, strategy):
    global simulation_target, simulation_count, current_start_word, stats

    simulation_target = n_games
    simulation_count = 0
    current_start_word = start_word

    stats[start_word] = {
        "games": 0,
        "wins": 0,
        "total_turns": 0,
        "greens": 0,
        "yellows": 0,
        "grays": 0
    }


    auto_play(strategy, start_word=start_word)

root.after(100, lambda: run_simulations("SLATE", 10, h.entropy))
#auto_play(h.entropy)
#print(feedback("APPLE", "ALERT"))
root.bind("<Return>", lambda event: submit_guess())
root.mainloop()

