import pandas as pd

def load_wordlist():
    df = pd.read_csv('wordle.csv')
    df.drop(['occurrence', 'day'], axis=1, inplace=True)
    return df['word'].str.upper().tolist()

wordlist = load_wordlist()