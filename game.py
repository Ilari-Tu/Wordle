import tkinter as tk
import pandas as pd
import random

df = pd.read_csv('wordle.csv')
df.drop(['occurrence', 'day'], axis=1, inplace=True)
#print(df)

correct_word = df['word'].sample(1).iloc[0].upper()

current_row = 0

def submit_guess():
    global current_row

    guess = "".join(cells[current_row][col].get().upper() for col in range (Columns))

    if len(guess) != Columns or not guess.isalpha():
        print("Incomplete or invalid guess")
        return
    
    if guess == correct_word:
        print("WIN", guess)
        end_game(win=True)
        return
    
    if current_row == Rows -1:
        print("LOSE", correct_word)
        end_game(win=False)
        return
    
    current_row += 1

def end_game(win):
    if win:
        print("You guessed correctly")
    else:
        print("Out of guesses")
    reset_game()

def reset_game():
    global current_row, correct_word
    current_row = 0

    # Clear all cells
    for r in range(Rows):
        for c in range(Columns):
            cells[r][c].delete(0, tk.END)
            cells[r][c].config(bg="white")

    # Pick a new word
    correct_word = df['word'].sample(1).iloc[0].upper()
    answer_label.config(text=f"Correct word (debug): {correct_word}")


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

answer_label = tk.Label(root, text=f"Correct word: {correct_word}", font=("Aerial", 12))
answer_label.grid(row=Rows +1, column=0, columnspan=Columns, pady=10)

root.bind("<Return>", lambda event: submit_guess())
root.mainloop()

