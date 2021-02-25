import random

def play():
    computer = random.choice(['p','s','r'])
    user = input(f'What\'s your choice? Paper(p), Scissor(s) or Rock(r)')

    if user == computer:
        return 'It\'s a tie'

    if is_win(user, computer):
        return f'You won! You\'er {user} and computer is {computer}'

    return f'You lost! You\'er {user} and computer is {computer}'

def is_win(user, opponent):
    if (user == 'p' and opponent == 'r') or (user == 'r' and opponent == 's') or (user == 's' and opponent == 'p'):
        return True

def start_Game():
    tryagain = True
    while tryagain:
        print(play())
        choose = input('Do you want to play again? Yes(y) or No(n)')
        if choose == 'n':
            tryagain = False

start_Game()