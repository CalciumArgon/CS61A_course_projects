## CATS 程序框架和细节处理

#### 框架

* Phase 1：对段落主题的选择，准确率统计，速度统计
* Phase 2：各种拼写纠错函数
* Phase 3：多人竞赛时的速度比较

#### 细节处理

1. `choose(paragraphs: list, select: func, k)` 函数要从段落里挑选出第 `k` 个满足一定特征的单词，要用 `select()` 作用在 `paragraph` 的每个单词上来判断是否满足所需要的特征（段落列表里的每个元素可能是一个长句子，不一定是单个单词）

    而这里的 `select(sentence: str)` 函数来自 `about(topic: list)` 产生的高阶函数

    用 map 和 lambda表达式将 `sentence` 变成逐个单词分割的、无标点的小写格式，这样可以对 `topic` 里所有词直接用 `in` 检验是否在其中
    ```python
    # 闭包函数
    def check_topic_in(sentence):
        word_list = list(map(lambda s: s.lower(), remove_punctuation(sentence).split(" ")))
        for topic_word in topic:
            if topic_word in word_list:
                return True
        return False
    ```

2. 给出了两种纠错方法： `sphinx_switches(start, goal, limit)` 和 `pawssible_patches(start, goal, limit)` ，它们都返回**最小需要的纠正步数**，这个数字将用于传入“单词替换函数”，用来反应每个单词到 `typed` 的“距离”，即用哪个单词来替换纠错正确率最高

    `sphinx_switches()` 是从左到右逐位纠错，当长度不相同时，很简单地把后面都切片去掉，并相应长度在 `limit` 中减去：
    ```python
    # len(start) < len(goal) 同理
    if len(start) > len(goal):
        return min(limit+1, len(start)-len(goal) + \
                            sphinx_switches(start[:len(goal)], 
                                            goal, 
                                            limit-(len(start)-len(goal))))
    # len(start) == len(goal) 时进入下面正常阶段
    ```

    正常情况下逐位比对，如果第一项不同就消耗一个 `limit` ，否则不消耗，都切片进入下一轮递归比较：
    ```python
    return min(limit+1, 
                int(start[0] != goal[0]) + sphinx_switches(start[1:], 
                    goal[1:], 
                    limit - int(start[0] != goal[0])))
    ```

    `pawssible_patches()` 则计算**在三种操作下的“最小距离”**（添加一位，去除一位，替换一位），首先要处理各种初始情况：
    ```python
    if limit == 0:  # 没有可操作空间
        return 0 if start == goal else 1
    elif len(start) * len(goal) == 0:   # 当一方没有剩余字符时剩下只能 全加/全减 操作
        return min(limit+1, abs(len(start) - len(goal)))
    elif start[0] == goal[0]:   # !!! 不要忘首位相同的初始情况 !!!
        return pawssible_patches(start[1:], goal[1:], limit)
    ```

    然后只判断第一位，剩下交给递归下一轮，返回对第一位的三种操作中最终最小的那种操作
    ```python
    # 每一种情况都对应消耗 1 步
    add = 1 + pawssible_patches(start, goal[1:], limit-1)
    remove = 1 + pawssible_patches(start[1:], goal, limit-1)
    substitute = 1 + pawssible_patches(start[1:], goal[1:], limit-1)

    return min(add, remove, substitute)
    ```
    这里和动态规划很像，实际可以创建 `len(start) * len(goal)` 的二维列表，每个格子都由周围格子的数字递推得来
    > TODO：写一遍动态规划求两字符串最短距离

3. 记录多人打字速度的核心就是 `time_per_word(times_per_player, words)` 函数

    用内置库来给每个单词打完后盖一个时间戳，
    ```python
    from datetime import datetime
    ```

    对每个 player 来说：（假设这里 `player` 是数字，可以作为索引）

    `times_per_player[player]` 是也一个列表，存放了该用户打每个单词完成时的时间戳，相当于存了一堆 `perf_counter()` ，要获得每个词的速度，要依次相减：
    ```python
    for player in range(len(times_per_player)):
        for i in range(len(words)):
            times_per_player[player][i] = times_per_player[player][i+1] - \
                                          times_per_player[player][i]
    ```
    
    然后要把每个列表的最后一项（最后一个单独的时间戳）去掉：
    
    :bangbang: 注意
    
    map() 返回一个 generator, 意味着里面内容不会被运行！

    只有加上 list() 全部迭代掉, 才会运行具体 lambda 函数！
    ```python
    # 如果不加 list 的话 each 不会有改变
    list(map(lambda each: each.pop(), times_per_player))
    ```

#### 待改进

1. 对拼写的纠正 `final_diff(start, goal, limit)` 仍使用默认的三种修改方式：加一位、删一位、替换一位；且修改次数相同时默认选取第一个单词，这说明该修改方法可能导致一个单词修改到很多单词上。

    所以，可以进一步通过对常见拼写错误的判断来增加修改正确率，比如 “xat” 按照现行方法改进可能是 “hat”，“rat” 等等，但实际键盘最有可能偏向的应是 “cat”。

2. 在 `utils.py` 中实际封装好了 `split()` `remove_punctuation()` ，可以自己实现：
   
   `split(string)` 函数就是直接返回 `string.split()`
   
   如 `split("aaa   bbb") -> ["aaa", "bbb"]` 一个神奇的的事情是，如果 `"aaa   bbb".split(" ")` 就只会按照一个空格划分变成 `['aaa', '', '', 'bbb']` ，而 `"aaa   bbb".split()` 会默认为所有的空字符，包括空格、换行(\n)、制表符(\t)等，全部去除

   `remove_punctuation(string)` 函数去除所有标点符号，返回新字符串

   使用了字符串的 `punctuation` `strip()` `translate()` 等内置方法
