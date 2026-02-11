import random
import math
from collections import Counter
from game_logic import feedback


def random_strategy(candidates):
    return random.choice(candidates)

def entropy(candidates):
    best_guess = None
    best_entropy = -1

    total = len(candidates)

    for guess in candidates[:20]:
        pattern_counts = Counter()

        for possible_answer in candidates:
            pattern = tuple(feedback(guess, possible_answer))
            pattern_counts[pattern] += 1

            entropy = 0
            for count in pattern_counts.values():
                p = count/total
                entropy -= p * math.log2(p)

                if entropy > best_entropy:
                    best_entropy = entropy
                    best_guess = guess
    
    return best_guess