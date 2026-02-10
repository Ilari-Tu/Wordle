current_row = 0

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

def single_game(answer,wordlist,strategy):
    candidates = wordlist.copy()
    guesses = []

    for _ in range(6):
        guess = strategy(candidates)
        guesses.append(guess)

        fb = feedback(guess, answer)

        if guess == answer:
            return True, guesses
        
        candidates = [w for w in candidates if feedback(guess,w) == fb]
    return False, guesses