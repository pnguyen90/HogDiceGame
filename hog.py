"""Contains the game logic components utilized by the GUI"""
from dice import *
from ucb import main, trace, log_current_line, interact
from random import randint

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.


######################
# Phase 1: Simulator #
######################

def make_test_dice(*outcomes):
    """Return a die that cycles deterministically through OUTCOMES.

    >>> dice = make_test_dice(1, 2, 3)
    >>> dice()
    1
    >>> dice()
    2
    >>> dice()
    3
    >>> dice()
    1
    >>> dice()
    2

    This function uses Python syntax/techniques not yet covered in this course.
    The best way to understand it is by reading the documentation and examples.
    """
    assert len(outcomes) > 0, 'You must supply outcomes to make_test_dice'
    for o in outcomes:
        assert type(o) == int and o >= 1, 'Outcome is not a positive integer'
    index = len(outcomes) - 1
    def dice():
        nonlocal index
        index = (index + 1) % len(outcomes)
        return outcomes[index]
    return dice


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 0.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN Question 1
    sum_dice = 0
    current_state = 0
    num_iterations = 0
    pig_out = 0
    while num_iterations < num_rolls:
        current_state = dice()
        if current_state != 1:
            sum_dice = sum_dice + current_state
            num_iterations += 1
        else:
            pig_out += 1
            num_iterations += 1
    if pig_out >= 1:
        sum_dice = 0
        return 0
    else:
        return sum_dice



    # END Question 1


def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= -1, 'Cannot roll less then negative two'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    # BEGIN Question 2

    def free_bacon(opponent_score):
        return largest_digit(opponent_score) + 1

    def largest_digit(n):
        y = n // 10
        x = n % 10
        return max(x,y)

    def is_prime(score):
        if score == 1 or score == 0:
            return False
        x = score-1
        while x > 1:
            if score % x == 0:
                return False
            else:
                x -= 1
        return True

    def next_prime(score):
        score += 1
        while not is_prime(score):
            score += 1
        return score
    def hogtimus_prime_check(score):
        if is_prime(score):
            return next_prime(score)
        else:
            return score
    if num_rolls == -1:
        return -1
    if num_rolls == 0:
        return hogtimus_prime_check(free_bacon(opponent_score))
    result = roll_dice(num_rolls, dice)

    return hogtimus_prime_check(result)

            # END Question 2


def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
    # BEGIN Question 3
    if (score + opponent_score) % 7 == 0:
        return four_sided
    else:
        return six_sided
    # END Question 3


def is_swap(score0, score1):
    """Returns whether the last two digits of SCORE0 and SCORE1 are reversed
    versions of each other, such as 19 and 91.
    """
    # BEGIN Question 4
    def swapper(score):
        tens = (score//10)%10
        ones = score%10
        swapped = 10*ones + tens
        return swapped
    def normalized(score):
        return score % 100
    if swapper(score0) == normalized(score1):
        return True
    else:
        return False

    # END Question 4


def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who

'''The play function below is the game state controller. It uses all the components implemented
above'''

def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    who = 0
    def play_my_turn(num_rolls, my_score, opponent_score):
        my_turn_score = take_turn(num_rolls, opponent_score, select_dice(my_score,opponent_score))
        return my_turn_score

    player0_pork_chop = 0
    player1_pork_chop = 0
    while (score0 < goal and score1 < goal):
        if who == 0:
            who = other(who)
            num_rolls = strategy0(score0, score1)
            turn_score = play_my_turn(num_rolls,score0,score1)
            if turn_score == -1 and player0_pork_chop == 0:
                score0, score1 = score1, score0
                player0_pork_chop = 1
            elif turn_score == -1 and player0_pork_chop == 1:
                turn_score = play_my_turn(10, score0, score1)
                if turn_score == 0:
                    score1 += 10
                    if is_swap(score0, score1):
                        score0, score1 = score1, score0
                else:
                    score0 += turn_score
                    if is_swap(score0, score1):
                        score0, score1 = score1, score0


            elif turn_score == 0:
                score1 += num_rolls
                if is_swap(score0, score1):
                    score0, score1 = score1, score0
            else:
                score0 += turn_score
                if is_swap(score0, score1):
                    score0, score1 = score1, score0

        else:
            who = other(who)
            num_rolls = strategy1(score1, score0)
            turn_score = play_my_turn(num_rolls,score1,score0)
            if turn_score == -1 and player1_pork_chop == 0:
                score0, score1 = score1, score0
                player1_pork_chop = 1
            elif turn_score == -1 and player1_pork_chop == 1:
                turn_score = play_my_turn(10, score1, score0)
                if turn_score == 0:
                    score0 += 10
                    if is_swap(score0, score1):
                        score0, score1 = score1, score0
                else:
                    score1 += turn_score
                    if is_swap(score0, score1):
                        score0, score1 = score1, score0
            elif turn_score == 0:
                score0 += num_rolls
                if is_swap(score0, score1):
                    score0, score1 = score1, score0
            else:
                score1 += turn_score
                if is_swap(score0, score1):
                    score0, score1 = score1, score0
    return score0, score1

"""Uncomment (un-string) the play function below if you would like to play without 'pork-chop' rule,
which is the rule where rolling 0 automatically swaps scores. Re-string this function to
play with pork chop rule.

def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    'This play function does not implement the pork chop rule'
    who = 0

    def play_my_turn(num_rolls, my_score, opponent_score):
        my_turn_score = take_turn(num_rolls, opponent_score,select_dice(my_score,opponent_score))
        return my_turn_score


    while (score0 < goal and score1 < goal):
        if who == 0:
            who = other(who)
            num_rolls = strategy0(score0, score1)
            turn_score = play_my_turn(num_rolls,score0,score1)
            if turn_score == 0:
                score1 += num_rolls
                if is_swap(score0, score1):
                    temp_score = score0
                    score0 = score1
                    score1 = temp_score
            else:
                score0 += turn_score
                if is_swap(score0, score1):
                    temp_score = score0
                    score0 = score1
                    score1 = temp_score

        else:
            who = other(who)
            num_rolls = strategy1(score1, score0)
            turn_score = play_my_turn(num_rolls,score1,score0)
            if turn_score == 0:
                score0 += num_rolls
                if is_swap(score0, score1):
                    temp_score = score0
                    score0 = score1
                    score1 = temp_score
            else:
                score1 += turn_score
                if is_swap(score0, score1):
                    temp_score = score0
                    score0 = score1
                    score1 = temp_score
    return score0, score1

    """


'''COPY AND PASTE THE STRATEGY YOU WANT TO PLAY AGAINST HERE. MAKE SURE THE STRATEGY NAME IS
'final_strategy' '''

## winning candidate
def final_strategy(score, opponent_score):
    bacon = take_turn(0, score, opponent_score)
    the_dice = select_dice(score , opponent_score)
    if the_dice == six_sided:
        margin = 7
    else:
        margin = 3
    def opt_num(dice, my_score, opponent_score):
        if dice == six_sided:

            if my_score >= 89:
                if bacon > margin:
                    return 0
                else:
                    return 2
            else:
                if bacon > margin:
                    return 0
                else:
                    return 4
        else:
            if my_score >= 93:
                if bacon > margin:
                    return 0
                else:
                    return 1
            else:
                if bacon > margin:
                    return 0
                else:
                    return 4
    def piggy_swap(score,opponent_score):
        if is_swap((opponent_score + 10), score) :
            return 10
        if is_swap((opponent_score + 9), score)  :
            return 9
        if is_swap((opponent_score + 8), score) :
            return 8
        if is_swap((opponent_score + 7), score) :
            return 7
        if is_swap((opponent_score + 6), score) :
            return 6
        if is_swap((opponent_score + 5), score) :
            return 5
        if is_swap((opponent_score + 4), score) :
            return 4
        if is_swap((opponent_score + 3), score) and the_dice == four_sided:
            return 3
        else:
            return False
    if opponent_score <= 80 and score <= 70:
        if piggy_swap(score, opponent_score) != False:
            return piggy_swap(score, opponent_score)
        else:
            return 7
    elif opponent_score >= 81 and score <= 70:
        return -1
    else:
        return opt_num(the_dice, score, opponent_score)







##########################
# Command Line Interface #
##########################






@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
