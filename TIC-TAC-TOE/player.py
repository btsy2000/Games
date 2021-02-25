import math
import random


class Player:
    def __init__(self, letter):
        # letter is X or O
        self.letter = letter

    # we want all player to get their next move given a game
    def get_move(self, game):
        pass


class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        # get a random available spot for our next move
        square = random.choice(game.available_moves())
        return square


class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + '\'s turn. Input move (0-8):')
            # we are going to check that this is a correct value by trying to cast
            # it to an integer, and if it's not, then we say its invalid
            # if that spot is not available in the board, we also say its invalid
            try:
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print('Invalid square. Try again')

        return val


class GeniusComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves())
        else:
            # get the square according to the minimax algorithm
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter  # yourself!!
        other_player = 'O' if player == 'X' else 'X'

        # first we want to check if the previous move is the winner
        # this is our base case
        if state.current_winner == other_player:
            # we should return position and score because we need to keep track the score
            # for minimax to work
            return {'position': None,
                    'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (
                                state.num_empty_squares() + 1)
                    }

        elif not state.empty_square():  # no empty square
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -math.inf}  # each score should maximize (be larger)
        else:
            best = {'position': None, 'score': math.inf}  # each score should minimize

        for possible_move in state.available_moves():
            # step1: make a move try that spot
            state.make_move(possible_move, player)
            # step2: recurse using minimax to simulate a game after making that move
            sim_score = self.minimax(state, other_player)  # now we alternate players

            # step3: undo the move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move  # otherwise this will get messed up from recursion

            # step4: update the dictionaries if necessary
            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score  # replace the best
            else:  # but minimax the other player
                if sim_score['score'] < best['score']:
                    best = sim_score  # replace the best

        return best
