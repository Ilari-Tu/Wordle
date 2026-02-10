from game_logic import feedback
from data import wordlist
from heuristics import random_strategy

import tkinter as tk
import random

answer = random.choice(wordlist)

current_row = 0

def submit_guess():
    global current_row

    guess = "".join(cells[current_row][col].get().upper() for col in range (Columns))

    if len(guess) != Columns or not guess.isalpha():
        print("Incomplete or invalid guess")
        return
    
    if guess == answer:
        print("WIN", guess)
        end_game(win=True)
        return
    
    if current_row == Rows -1:
        print("LOSE", answer)
        end_game(win=False)
        return

    colors = feedback(guess, answer)

    for col in range(Columns):
        cells[current_row][col].config(bg=colors[col])

    current_row += 1

def end_game(win):
    if win:
        print("You guessed correctly")
    else:
        print("Out of guesses")
    reset_game()

"""
def feedback(guess, answer):
    guess = guess.upper()
    answer = answer.upper()

    result = ['gray']*len(guess)
    answer_chars = list(answer)

    for i in range(len(guess)):
        if guess[i] == answer[i]:
            result[i] = "green"
            answer_chars[i] = None

    for i in range(len(guess)):
        if result[i] == "green":
            continue
        if guess[i] in answer_chars:
            result[i] = "yellow"
            answer_chars[answer_chars.index(guess[i])] = None
    return result
"""
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

def auto_play(strategy):
    candidates = wordlist.copy()

    def step():
        nonlocal candidates

        guess = strategy(candidates)
        done = play_guess(guess)

        if done:
            return
        
        fb = feedback(guess, answer)
        candidates = [w for w in candidates if feedback(guess, w) == fb]

        root.after(700, step)
    
    step()

auto_play(random_strategy)
#print(feedback("APPLE", "ALERT"))
root.bind("<Return>", lambda event: submit_guess())
root.mainloop()

