"""Typing test implementation"""

from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns True. If there are fewer than K such paragraphs, return
    the empty string.

    Arguments:
        paragraphs: a list of strings
        select: a function that returns True for paragraphs that can be selected
        k: an integer

    >>> ps = ['hi', 'how are you', 'fine']
    >>> s = lambda p: len(p) <= 4
    >>> choose(ps, s, 0)
    'hi'
    >>> choose(ps, s, 1)
    'fine'
    >>> choose(ps, s, 2)
    ''
    """
    # BEGIN PROBLEM 1
    valid = []
    for string in paragraphs:
        if select(string):
            valid.append(string)
    try:
        return valid[k]
    except IndexError:
        return ""
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether
    a paragraph contains one of the words in TOPIC.

    Arguments:
        topic: a list of words related to a subject

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    def check_topic_in(sentence):
        word_list = list(map(lambda s: s.lower(), remove_punctuation(sentence).split(" ")))
        for topic_word in topic:
            if topic_word in word_list:
                return True
        return False
    return check_topic_in
    # END PROBLEM 2


def accuracy(typed, reference) -> float:
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    Arguments:
        typed: a string that may contain typos
        reference: a string without errors

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    >>> accuracy('', '')
    100.0

    !!  Tabs DON't counts
    !!  Punctuations counts

    """
    typed_words = split(typed)  # 只消除空格, 每个单词保留符号 (在左右或内部都保留)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    lt, lr = len(typed_words), len(reference_words)
    if lt * lr == 0:
        if lt == 0 and lr == 0: # 全为 0 时正确率 100.0
            return 100.0
        return 0.0  # 否则只有一个为 0 正确率 0.0

    wrong = 0   # 记录错误的单词数量
    for i in range(lt):
        try:
            if typed_words[i] != reference_words[i]:
                wrong += 1
            continue
        except IndexError:  # 如果超过 reference_word 长度则都算错误单词
            wrong += 1
            continue
    return float(100 * (lt - wrong) / lt)
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string.

    Arguments:
        typed: an entered string
        elapsed: an amount of time in seconds

    >>> wpm('hello friend hello buddy hello', 15)
    24.0
    >>> wpm('0123456789',60)
    2.0

    !!  Concluding punctuation !!
    """
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    words = repr(typed)[1:len(typed)+1]     # repr() 函数返回的字符串包含左右两引号, 把两端切掉
    return float(len(words) / 5) * float(60 / elapsed)
    # END PROBLEM 4


###########
# Phase 2 #
###########

def autocorrect(typed_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from TYPED_WORD. Instead returns TYPED_WORD if that difference is greater
    than LIMIT.

    Arguments:
        typed_word: a string representing a word that may contain typos
        valid_words: a list of strings representing valid words
        diff_function: a function quantifying the difference between two words
        limit: a number

    >>> ten_diff = lambda w1, w2, limit: 10 # Always returns 10
    >>> autocorrect("hwllo", ["butter", "hello", "potato"], ten_diff, 20)
    'butter'
    >>> first_diff = lambda w1, w2, limit: (1 if w1[0] != w2[0] else 0) # Checks for matching first char
    >>> autocorrect("tosting", ["testing", "asking", "fasting"], first_diff, 10)
    'testing'

    !!  Assume NO punctuation.
    !! Using the 'key' argument in min() and max()
    """
    # BEGIN PROBLEM 5
    if typed_word in valid_words:
        return typed_word
    
    diff = []
    for i in range(len(valid_words)):
        diff.append(diff_function(typed_word, valid_words[i], limit))
    if min(diff) > limit:
        return typed_word
    else:
        return valid_words[diff.index(min(diff))]

    # END PROBLEM 5


def sphinx_switches(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths and returns the result.

    Arguments:
        start: a starting word
        goal: a string representing a desired goal word
        limit: a number representing an upper bound on the number of chars that must change

    >>> big_limit = 10
    >>> sphinx_switches("nice", "rice", big_limit)    # Substitute: n -> r
    1
    >>> sphinx_switches("range", "rungs", big_limit)  # Substitute: a -> u, e -> s
    2
    >>> sphinx_switches("pill", "pillage", big_limit) # Don't substitute anything, length difference of 3.
    3
    >>> sphinx_switches("roses", "arose", big_limit)  # Substitute: r -> a, o -> r, s -> o, e -> s, s -> e
    5
    >>> sphinx_switches("rose", "hello", big_limit)   # Substitute: r->h, o->e, s->l, e->l, length difference of 1.
    5
    """
    # BEGIN PROBLEM 6
    if len(start) > len(goal):
        return min(limit+1, len(start)-len(goal) + sphinx_switches(start[:len(goal)], goal, limit-(len(start)-len(goal))))
    elif len(start) < len(goal):
        return min(limit+1, len(goal)-len(start) + sphinx_switches(start, goal[:len(start)], limit-(len(goal)-len(start))))
    
    # 下面是长度相等的情况
    if len(start) == 0:     # 初始情况 1: 字符全部判断完成
        return 0
    if limit == 0:          # 初始情况 2: limit 达到 0 之后不再进行多余判断
        if start != goal:
            return 1        # 不相同就只比 limit 多返回 1
        return 0
    return min(limit+1, int(start[0] != goal[0]) + sphinx_switches(start[1:], goal[1:], limit - int(start[0] != goal[0])))
    # END PROBLEM 6


# -------------------------------------
# 类似动态规划
# 当某一位不一样的时候, 有三种方法让这位一样
# 在前面添加一位; 将这位减去; 将第一位替换掉
# 只需要取这三种的最小值即可
# 而这三种操作分别都可以用递归函数表示出来
#
# 所以, 用二维列表递推每一位也是可以的
# -------------------------------------
def pawssible_patches(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL.
    This function takes in a string START, a string GOAL, and a number LIMIT.

    Arguments:
        start: a starting word
        goal: a goal word
        limit: a number representing an upper bound on the number of edits

    >>> big_limit = 10
    >>> pawssible_patches("cats", "scat", big_limit)       # cats -> scats -> scat
    2
    >>> pawssible_patches("purng", "purring", big_limit)   # purng -> purrng -> purring
    2
    >>> pawssible_patches("ckiteus", "kittens", big_limit) # ckiteus -> kiteus -> kitteus -> kittens
    3
    """
    if limit == 0:  # Fill in the condition
        # BEGIN
        return 0 if start == goal else 1
        # END

    elif len(start) * len(goal) == 0:  # Feel free to remove or add additional cases
        # BEGIN
        return min(limit+1, abs(len(start) - len(goal)))
        # END

    elif start[0] == goal[0]:   # 不要忘首位相同的初始情况
        return pawssible_patches(start[1:], goal[1:], limit)

    else:
        # 每一种情况都对应消耗 1 步
        add = 1 + pawssible_patches(start, goal[1:], limit-1)
        remove = 1 + pawssible_patches(start[1:], goal, limit-1)
        substitute = 1 + pawssible_patches(start[1:], goal[1:], limit-1)
        # BEGIN
        return min(add, remove, substitute)
        # END


def final_diff(start, goal, limit):
    """A diff function that takes in a string START, a string GOAL, and a number LIMIT.
    If you implement this function, it will be used."""
    '''------- For pawssible_patches() ---------
    | Correction Speed: 922.4502561147335 wpm   |
    | Correctly Corrected: 452 words            |
    | Incorrectly Corrected: 192 words          |
    | Uncorrected: 49 words                     |
    ------------------------------------------'''
    return pawssible_patches(start, goal, limit)


FINAL_DIFF_LIMIT = 6  # REPLACE THIS WITH YOUR LIMIT


###########
# Phase 3 #
###########


def report_progress(typed, prompt, user_id, send):
    """Send a report of your id and progress so far to the multiplayer server.
    Returns the progress so far.

    Arguments:
        typed: a list of the words typed so far
        prompt: a list of the words in the typing prompt
        user_id: a number representing the id of the current user
        send: a function used to send progress to the multiplayer server

    >>> print_progress = lambda d: print('ID:', d['id'], 'Progress:', d['progress'])
    >>> # The above function displays progress in the format ID: __, Progress: __
    >>> print_progress({'id': 1, 'progress': 0.6})
    ID: 1 Progress: 0.6
    >>> typed = ['how', 'are', 'you']
    >>> prompt = ['how', 'are', 'you', 'doing', 'today']
    >>> report_progress(typed, prompt, 2, print_progress)
    ID: 2 Progress: 0.6
    0.6
    >>> report_progress(['how', 'aree'], prompt, 3, print_progress)
    ID: 3 Progress: 0.2
    0.2
    """
    # BEGIN PROBLEM 8
    correct = 0
    for i in range(len(typed)):
        if typed[i] == prompt[i]:
            correct += 1
            continue
        break
    send({"id": user_id, "progress": correct / len(prompt)})
    print(correct / len(prompt))
    # END PROBLEM 8


def fastest_words_report(times_per_player, words):
    """Return a text description of the fastest words typed by each player."""
    game = time_per_word(times_per_player, words)
    fastest = fastest_words(game)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def time_per_word(times_per_player, words):
    """Given timing data, return a game data abstraction, which contains a list
    of words and the amount of time each player took to type each word.

    Arguments:
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.
        words: a list of words, in the order they are typed.

    >>> p = [[75, 81, 84, 90, 92], [19, 29, 35, 36, 38]]
    >>> game = time_per_word(p, ['collar', 'plush', 'blush', 'repute'])
    >>> all_words(game)
    ['collar', 'plush', 'blush', 'repute']
    >>> all_times(game)
    [[6, 3, 6, 2], [10, 6, 1, 2]]

    # words 存在第 1 项
    # times 存在第 2 项
    """
    # BEGIN PROBLEM 9
    for each in range(len(times_per_player)):
        for i in range(len(words)):
            times_per_player[each][i] = times_per_player[each][i+1] - times_per_player[each][i]\
    
    # !!! map() 返回一个 generator, 意味着里面内容不会被运行
    # 只有加上 list() 全部迭代掉, 才会运行具体 lambda 函数
    list(map(lambda each: each.pop(), times_per_player))
    
    return game(words, times_per_player)
    # END PROBLEM 9


def fastest_words(game):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        game: a game data abstraction as returned by time_per_word.

    >>> p0 = [5, 1, 3]
    >>> p1 = [4, 1, 6]
    >>> fastest_words(game(['Just', 'have', 'fun'], [p0, p1]))
    [['have', 'fun'], ['Just']]

    game[0] -> words
    game[1] -> times
    """
    player_indices = range(len(all_times(game)))  # contains an *index* for each player
    word_indices = range(len(all_words(game)))    # contains an *index* for each word
    # BEGIN PROBLEM 10
    fast = [[] for _ in player_indices]
    for i in word_indices:
        each_players_time = [all_times(game)[player][i] for player in player_indices]
        fast[each_players_time.index(min(each_players_time))].append(all_words(game)[i])
    return fast
    # END PROBLEM 10


def game(words, times):
    """A data abstraction containing all words typed and their times."""
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return [words, times]


def word_at(game, word_index):
    """A selector function that gets the word with index word_index"""
    assert 0 <= word_index < len(game[0]), "word_index out of range of words"
    return game[0][word_index]


def all_words(game):
    """A selector function for all the words in the game"""
    return game[0]


def all_times(game):
    """A selector function for all typing times for all players"""
    return game[1]


def time(game, player_num, word_index):
    """A selector function for the time it took player_num to type the word at word_index"""
    assert word_index < len(game[0]), "word_index out of range of words"
    assert player_num < len(game[1]), "player_num out of range of players"
    return game[1][player_num][word_index]


def game_string(game):
    """A helper function that takes in a game object and returns a string representation of it"""
    return "game(%s, %s)" % (game[0], game[1])


enable_multiplayer = False  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
