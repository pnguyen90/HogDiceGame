from dice import *
from hog import *

#######################
# Phase 2: Strategies #
#######################
# This file is the testing ground for strategies. first make your strategy or strategies.
# To run your strategy against another one, modify the run_experiments function.
#
# Experiments
"""Below are some functions used to play strategies against each other and
find out statistical advantages of one strategy over another"""

'''Below is our first super basic strategy.'''
def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n

    return strategy

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    5.5

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 0.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 5.5.
    Note that the last example uses roll_dice so the hogtimus prime rule does
    not apply.
    """
    # BEGIN Question 6

    def helper(*args):
        sum = 0
        count = 0
        while (count < num_samples):
            sum += fn(*args)
            count += 1
        return sum/num_samples

    return helper

    # END Question 6


def max_scoring_num_rolls(dice=six_sided, num_samples=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE over NUM_SAMPLES times.
    Assume that dice always return positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    # BEGIN Question 7

    def roll_n(n):
        return roll_dice(n, dice)

    n = 1
    top_score = 0
    top_dice_num = 1
    current_score = 0
    while (n < 11):
        current_score = make_averaged(roll_n, num_samples)(n)
        if (current_score > top_score):
            top_score = current_score
            top_dice_num = n
        n += 1
    return top_dice_num






    # END Question 7


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    win_rate_as_player_0 = 1 - make_averaged(winner,10000)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner,10000)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    if False:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False:  # Change to True to test always_roll(8)
        print('always_roll(2) win rate:', average_win_rate(always_roll(3)))

    if False:  # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False:  # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if True:  # Change to True to test final_strategy
        print ('final_strategy win rate:', average_win_rate(final_strategy,always_roll(5)))


# Strategies
"""Below are various hog strategy functions"""

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n

    return strategy



def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 8
    "*** REPLACE THIS LINE ***"
    if margin <= take_turn(0,opponent_score, select_dice(score,opponent_score)):
        return 0
    else:
        return num_rolls  # Replace this statement
    # END Question 8


def swap_strategy(score, opponent_score, num_rolls=5):
    """This strategy rolls 0 dice when it results in a beneficial swap and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN Question 9
    score += take_turn(0,opponent_score,select_dice(score,opponent_score))
    if is_swap(score, opponent_score) and (opponent_score > score):
        return 0
    else:
        return num_rolls  # Replace this statement
    # END Question 9



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
