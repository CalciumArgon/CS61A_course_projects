"""CS 61A Presents The Game of Hog."""

from dice import six_sided, four_sided, make_test_dice
from ucb import main, trace, interact
from functools import reduce

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################


def roll_dice(num_rolls, dice=six_sided):
    """Simulate rolling the DICE exactly NUM_ROLLS > 0 times. Return the sum of
    the outcomes unless any of the outcomes is 1. In that case, return 1.

    num_rolls:  The number of dice rolls that will be made.
    dice:       A function that simulates a single dice roll outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    # BEGIN PROBLEM 1
    # !!! Make sure call the dice exactly num_rolls times, even though 1 occured.
    # !!! Otherwise, the cycle in make_test_dice() stops in wrong place.
    numbers = []
    for _ in range(num_rolls):
        numbers.append(dice())
    return 1 if 1 in numbers else sum(numbers)
    # END PROBLEM 1


def piggy_points(score):
    """Return the points scored from rolling 0 dice.

    score:  The opponent's current score.
    """
    # BEGIN PROBLEM 2
    if score == 0:
        return 3
    tot = score ** 2
    minimum = 9
    while tot > 0:
        minimum = min(tot % 10, minimum)
        tot //= 10
    return minimum + 3
    # END PROBLEM 2


def take_turn(num_rolls, opponent_score, dice=six_sided, goal=GOAL_SCORE):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 in the case
    of a player using Piggy Points.
    Return the points scored for the turn by the current player.

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function that simulates a single dice roll outcome.
    goal:            The goal score of the game.
    """
    # Leave these assert statements here; they help check for errors.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice in take_turn.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < goal, 'The game should be over.'
    # BEGIN PROBLEM 3
    if num_rolls == 0:
        return piggy_points(opponent_score)
    return roll_dice(num_rolls, dice)
    # END PROBLEM 3


def more_boar(player_score, opponent_score):
    """Return whether the player gets an extra turn.

    player_score:   The total score of the current player.
    opponent_score: The total score of the other player.

    >>> more_boar(21, 43)
    True
    >>> more_boar(22, 43)
    True
    >>> more_boar(43, 21)
    False
    >>> more_boar(12, 12)
    False
    >>> more_boar(7, 8)
    False
    """
    # BEGIN PROBLEM 4
    # !!! Only check the two [leftmost] number of the score 
    opponent = str(opponent_score)
    player = str(player_score)
    opponent = "0" * (2 - len(opponent)) + opponent
    player = "0" * (len(opponent) - len(player)) + player

    if int(player[0]) < int(opponent[0]) and \
        int(player[1]) < int(opponent[1]):
        return True
    return False
    # END PROBLEM 4


def next_player(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> next_player(0)
    1
    >>> next_player(1)
    0
    """
    return 1 - who


def silence(score0, score1):
    """Announce nothing (see Phase 2)."""
    return silence


def play(strategy0, strategy1, score0=0, score1=0, dice=six_sided,
         goal=GOAL_SCORE, say=silence):
    """Simulate a game and return the final scores of both players, with Player
    0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    score0:     Starting score for Player 0
    score1:     Starting score for Player 1
    dice:       A function of zero arguments that simulates a dice roll.
    goal:       The game ends and someone wins when this score is reached.
    say:        The commentary function to call at the end of the first turn.
    """
    who = 0  # Who is about to take a turn, 0 (first) or 1 (second)
    # BEGIN PROBLEM 5
    strategy = [strategy0, strategy1]
    score = [score0, score1]
    while score[0] < goal and score[1] < goal:
        time = strategy[who](score[who], score[1-who])
        score[who] += take_turn(time, score[1-who], dice, goal)
        who = next_player(who) if more_boar(score[who], score[1-who]) == False else who
        # BEGIN PROBLEM 6
        say = say(score[0], score[1])
        # END PROBLEM 6
    # END PROBLEM 5    
    return score[0], score[1]


#######################
# Phase 2: Commentary #
#######################


def say_scores(score0, score1):
    """A commentary function that announces the score for each player."""
    print("Player 0 now has", score0, "and Player 1 now has", score1)
    return say_scores


def announce_lead_changes(last_leader=None):
    """Return a commentary function that announces lead changes.

    >>> f0 = announce_lead_changes()
    >>> f1 = f0(5, 0)
    Player 0 takes the lead by 5
    >>> f2 = f1(5, 12)
    Player 1 takes the lead by 7
    >>> f3 = f2(8, 12)
    >>> f4 = f3(8, 13)
    >>> f5 = f4(15, 13)
    Player 0 takes the lead by 2
    """
    def say(score0, score1):
        if score0 > score1:
            leader = 0
        elif score1 > score0:
            leader = 1
        else:
            leader = None
        if leader != None and leader != last_leader:
            print('Player', leader, 'takes the lead by', abs(score0 - score1))
        return announce_lead_changes(leader)
    return say


def both(f, g):
    """Return a commentary function that says what f says, then what g says.

    NOTE: the following game is not possible under the rules, it's just
    an example for the sake of the doctest

    >>> h0 = both(say_scores, announce_lead_changes())
    >>> h1 = h0(10, 0)
    Player 0 now has 10 and Player 1 now has 0
    Player 0 takes the lead by 10
    >>> h2 = h1(10, 8)
    Player 0 now has 10 and Player 1 now has 8
    >>> h3 = h2(10, 17)
    Player 0 now has 10 and Player 1 now has 17
    Player 1 takes the lead by 7
    """
    def say(score0, score1):
        return both(f(score0, score1), g(score0, score1))
    return say


def announce_highest(who, last_score=0, running_high=0):
    """Return a commentary function that announces when WHO's score
    increases by more than ever before in the game.

    NOTE: the following game is not possible under the rules, it's just
    an example for the sake of the doctest

    >>> f0 = announce_highest(1) # Only announce Player 1 score gains
    >>> f1 = f0(12, 0)
    >>> f2 = f1(12, 9)
    Player 1 has reached a new maximum point gain. 9 point(s)!
    >>> f3 = f2(20, 9)
    >>> f4 = f3(20, 30)
    Player 1 has reached a new maximum point gain. 21 point(s)!
    >>> f5 = f4(20, 47) # Player 1 gets 17 points; not enough for a new high
    >>> f6 = f5(21, 47)
    >>> f7 = f6(21, 77)
    Player 1 has reached a new maximum point gain. 30 point(s)!
    """
    assert who == 0 or who == 1, 'The who argument should indicate a player.'
    # BEGIN PROBLEM 7
    def say(score0, score1):
        score = [score0, score1]
        # nonlocal last_score
        # nonlocal running_high     # !!! Do not modify those initial arguments
        diff = score[who] - last_score
        if diff > running_high:
            print(f"Player {who} has reached a new maximum point gain. {diff} point(s)!")
            temp_running_high = diff
        else:
            temp_running_high = running_high
        return announce_highest(who, last_score=score[who], running_high=temp_running_high)
    return say
    # END PROBLEM 7


#######################
# Phase 3: Strategies #
#######################


def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments (the
    current player's score, and the opponent's score), and returns a number of
    dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return n
    return strategy


def make_averaged(original_function, trials_count=1000):
    """Return a function that returns the average value of ORIGINAL_FUNCTION
    when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(4, 2, 5, 1)
    >>> averaged_dice = make_averaged(roll_dice, 1000)
    >>> averaged_dice(1, dice)
    3.0
    """
    # make_average()() 二阶函数输出的是给定函数的多次return值的平均

    # BEGIN PROBLEM 8
    def evaluate(*arg):
        cnt = [None] * trials_count
        for i in range(trials_count):
            cnt[i] = original_function(*arg)
        avg = sum(cnt) / trials_count
        return avg
    return evaluate
    # END PROBLEM 8


def max_scoring_num_rolls(dice=six_sided, trials_count=1000):
    """Return the number of dice (1 to 10) that gives the highest average turn score
    by calling roll_dice with the provided DICE a total of TRIALS_COUNT times.
    Assume that the dice always return positive outcomes.

    >>> dice = make_test_dice(1, 6)
    >>> max_scoring_num_rolls(dice)
    1
    """
    # BEGIN PROBLEM 9
    avg = [None] * 10
    check_dice = make_averaged(roll_dice, trials_count=trials_count)
    for i in range(10):
        avg[i] = check_dice(i+1, dice)
    maximum = max(avg)
    return avg.index(maximum) + 1
    # END PROBLEM 9


def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(strategy, baseline=always_roll(6)):
    """Return the average win rate of STRATEGY against BASELINE. Averages the
    winrate when starting the game as player 0 and as player 1.
    """
    # winner 函数的输出正好是 0/1, 输出的平均直接等于胜率
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)

    return (win_rate_as_player_0 + win_rate_as_player_1) / 2


def run_experiments():
    """Run a series of strategy experiments and report results."""
    six_sided_max = max_scoring_num_rolls(six_sided)
    print('Max scoring num rolls for six-sided dice:', six_sided_max)
    for i in range(1, 11):
        print(f'always_roll({i}) win rate:', average_win_rate(always_roll(i)))

    #print('always_roll(8) win rate:', average_win_rate(always_roll(8)))
    #print('piggypoints_strategy win rate:', average_win_rate(piggypoints_strategy))
    #print('more_boar_strategy win rate:', average_win_rate(more_boar_strategy))
    #print('final_strategy win rate:', average_win_rate(final_strategy))
    "*** You may add additional experiments as you wish ***"


def piggypoints_strategy(score, opponent_score, cutoff=8, num_rolls=6):
    """This strategy rolls 0 dice if that gives at least CUTOFF points, and
    rolls NUM_ROLLS otherwise.
    """
    # BEGIN PROBLEM 10
    piggy = piggy_points(opponent_score)
    return 0 if piggy >= cutoff else num_rolls
    # END PROBLEM 10


def more_boar_strategy(score, opponent_score, cutoff=8, num_rolls=6):
    """This strategy rolls 0 dice when it triggers an extra turn. It also
    rolls 0 dice if it gives at least CUTOFF points and does not give an extra turn.
    Otherwise, it rolls NUM_ROLLS.
    """
    # BEGIN PROBLEM 11
    piggy = piggy_points(opponent_score)
    if piggy >= cutoff or more_boar(score + piggy, opponent_score) == True:
        return 0
    else:
        return num_rolls
    # END PROBLEM 11

def larger_than_rate(target, rate, trials_count=1000, dice=six_sided) -> int:
    for i in range(10):
        rate_of_i = 0
        for _ in range(trials_count):
            if roll_dice(i+1, dice) >= target:
                rate_of_i += 1
        if rate_of_i / trials_count >= rate:
            return i + 1
    return None

def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    # BEGIN PROBLEM 12
    # Special Cases:
    # 1. piggy_point is enough to reach the GOAL
    if piggy_points(opponent_score) >= GOAL_SCORE - score:
        return 0
    # 2. Distance to goal <= 10 points, and far from opponent >= 20, keep steady
    if GOAL_SCORE - score <= 10 and score - opponent_score >= 20:
        steady =  larger_than_rate(5 + (score-15-opponent_score)//10,
                            max(0.5, 0.65-(score-15-opponent_score)//10))
        if steady != None:
            return steady
    # 3. Be more aggressive if last rolling contains 1 ???
    # 4. Default
    return more_boar_strategy(score, opponent_score, cutoff=9, num_rolls=6)
    # END PROBLEM 12

##########################
# Command Line Interface #
##########################

# NOTE: Functions in this section do not need to be changed. They use features
# of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')

    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()


if __name__ == '__main__':
    print("TEST HERE")
    for i in range(1, 11):
        # print(i, max_scoring_num_rolls(six_sided))
        print(i, make_averaged(roll_dice)(i, six_sided))
    print(larger_than_rate(6, 0.6))
