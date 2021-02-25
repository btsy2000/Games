import random
from words import words
import string

def get_valid_word(words):
    word = random.choice(words)

    while '-' in word or ' ' in word:
        word = random.choice(words)

    print(word)
    return  word

def hangman():
    word = get_valid_word(words)
    word_letters = set(word)  # letter in the word
    alphabet = set(string.ascii_uppercase)
    used_letters = set()    # used for user guess

    lives = len(word_letters) + 5

    # Get user input
    while len(word_letters) > 0 and lives > 0:
        # Letter used from ' '.join(['a', 'b', 'c']) -> 'a b c'
        print('You have', lives, 'lives left and those letters has been used: ', ' '.join(used_letters))

        # What current word is
        word_list = [letter if letter.upper() in used_letters else '-' for letter in word]
        print('Current word: ', ' '.join(word_list))

        user_letter = input('Guess a letter: ').upper()
        # print(f'input letter = {user_letter} and used_letters = { str(used_letters)}, word letter is {str(word_letters)}')
        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            if user_letter.lower() in word_letters:
                word_letters.remove(user_letter.lower())

            else:
                lives = lives - 1   # take a life away
                print('letter is not in word!\n')

        elif user_letter in used_letters:
            print('this letter is used, try another letter\n')

        else:
            print('Invalid character! Please try again.\n')


    # When the lenth of letter is == 0
    if lives > 0:
        print(f'Congratulations! The word is \"{word}\", you did it.')

    else:
        print('Sorry you die! the word is', word, '!!!')

hangman()
