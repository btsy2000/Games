import random

def user_guess(x):
    random_number = random.randint(1, x)
    count = 0
    guess = 0
    while guess != random_number:
        guess = int(input(f'Guess a number between 1 to {x}: '))
        count = count + 1
        if guess < random_number:
            print(f'the guess number {guess} is too blow')
        elif guess > random_number:
            print(f'the guess number {guess} is too high')

    print(f'Congratulations! You had guessed {count} times to got it.')

def computer_guess(x):
    count = 0
    low = 1
    high = x
    feedback = ''
    while  feedback != 'c':
        count = count +1
        if low != high:
            guess = random.randint(low, high)
        else:
            guess = low
        feedback = input(f'Is {guess} is too high(H), or too low(L), or correct(C)?').lower()
        if feedback == 'h':
            high = guess -1
        elif feedback == 'l':
            low = guess +1
        elif feedback != 'c':
            print('please input the correct feedback: High(h), Low(l) or Correct(c)!')
            count = count -1
    print(f'Congratulation! The computer guessed our number {guess}, after {count} times!')

computer_guess(1000)
# user_guess(1000)