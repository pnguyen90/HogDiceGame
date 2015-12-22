This project was assigned by Professor John Denero for CS61A at UC Berkeley.


The files that constitue my work (Phong Nguyen) are the hog.py and strategies.py files.

The rest of the helper files and the gui were provided by John Denero.



**********

To play a game of hog against another human (on the same computer), run the command below:

python hog_gui.py


**********

To play against the strategy currently in the hog.py file, run the command below:

python hog_gui.py -f

**********


If you would like to write new strategy functions and test them against some given baseline strategies, or even pit 
two of your own against each other, write them into the strategies.py file, then modify the run_experiments function.


To see the win/loss results averaged over 1000 games, run the command below in sequence:

python -i strategies.py
python run_experiments()

**********

If you would like to play against another strategy function, copy and paste it over the final_strategy function 
given in hog.py.    Make sure to rename your new function 'final_strategy' function.


**********

If you would like to play the game without the pork chop rule, uncomment the second play function given in hog.py
Make sure if you play against a strategy function, the strategy function does not assume pork chop is
a valid rule.



THE RULES OF HOG ARE BELOW:::::::::::::::::::::::::::::::::::::::





    Pig Out. If any of the dice outcomes is a 1, the current player's score for the turn is 0.


    Piggy Back. When the current player scores 0, the opposing player receives points equal to the number of dice rolled that turn.
        Example: If the current player rolls 3 dice that come up 1, 5, and 1, then the current player scores 0 and the opponent scores 3.


    Free Bacon. A player who chooses to roll zero dice scores one more than the largest digit in the opponent's total score.
        Example 1: If the opponent has 42 points, the current player gains 1 + max(4, 2) = 5 points by rolling zero dice.
        Example 2: If the opponent has has 48 points, the current player gains 1 + max(4, 8) = 9 points by rolling zero dice.
        Example 3: If the opponent has has 7 points, the current player gains 1 + max(0, 7) = 8 points by rolling zero dice.


    Hog Wild. If the sum of both players' total scores is a multiple of seven (e.g., 14, 21, 35), then the current player rolls four-sided dice instead of the usual six-sided dice.


    Hogtimus Prime. If a player's score for the turn is a prime number, then the turn score is increased to the next largest prime number.
                   For example, if the dice outcomes sum to 19, the current player scores 23 points for the turn. This boost only applies
                   to the current player. Note: 1 is not a prime number!


    Swine Swap. After the turn score is added, if the last two digits of each player's score are the reverse of each other, the players swap total scores.



    Pork Chop (New!). A player may choose to roll -1 dice, which scores no points for the turn, but swaps both players' scores (similar to Swine Swap). 
                   This move can only be used once by each player; every subsequent roll of -1 will be treated as if that player rolled 10 dice instead.

                  Note: If Swine Swap would trigger immediately after Pork Chop, that swap doesn't take effect! There can be at most one swap per turn.
              
        