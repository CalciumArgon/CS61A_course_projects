## hog 程序框架

1. Powershell 测试/提交命令

一共 12 个 Problem，每个 Problem 有理解性测试和代码测试两部分

理解性测试，针对规则的理解，自己运算相应函数的输出结果
```powershell
python ok -q 01 -u --local
```

代码测试（不加 `-i` 也可以），不加 `-q 0X` 就是全部代码测试
```powershell
python ok -q 01 -i --local
python ok --local
```

查看测试分数
```powershell
python ok --score --local
```

运行 `run_experiments()` 函数，里面可以进行测试，这样可以不用 `if __name__ == "__main__"` 来写
```powershell
python3 hog.py -r
```

运行 GUI 网页模拟，可以双人对战，也可以单人与自己写的 final_strategy 对战
```powershell
python hog_gui.py
```

2. `dice.py`

提供了正常的骰子 `six_sided` 和 按照指定结果依次循环输出的测试骰子 `make_test_dice(*outcomes)`

3. `hog.py`

    * Phase 1: Simulator

    实现各种规则，piggy_point 对应 `roll_dice(0)` 获得对手总分的平方的最小位数加三，more_boar 判断是否最左两位均小于对方最左两位以获得新回合，注意若到达两位则不需要补零，比如 `more_boar(100, 22)` 应当返回 `True`

    核心模拟函数 `play()`
    
    `strategy(score, opponent_score)` 是决策函数，接收双方当下分数并返回下一次应当扔的次数，`take_turn()` 按照相应规则扔骰子并返回获得的分数，`say(score0, score1)` 是解说函数，打印解说内容，并返回另一个相同功能但初始参数不同的新 `say` 函数，从而在下一轮进入 while 循环反复调用，在 Phase 2 完成。
    ```python
    def play(strategy0, strategy1, score0=0, score1=0, dice=six_sided, \
            goal=GOAL_SCORE, say=silence):
        who = 0
        strategy = [strategy0, strategy1]   # 打包从而能用 who 索引调用
        score = [score0, score1]
        while score[0] < goal and score[1] < goal:  # 一直模拟到游戏结束
            time = strategy[who](score[who], score[1-who])  # 决策扔的次数
            score[who] += take_turn(time, score[1-who], dice, goal) # take_turn执行扔的次数
            who = next_player(who) if more_boar(score[who], score[1-who]) == False \
                                   else who # 判断是否触发 more_boar, 即决定 who 的下一轮赋值
            say = say(score[0], score[1])   # 对当前得分的解说 print 结果并返回另一个 say 函数
        return score[0], score[1]
    ```

    * Phase 2: Commentary

    认真学习代码结构，高阶函数的应用

    * Phase 3: Strategies

    `make_averaged()` 是计算某个函数某种运行方式的均值（在该运行方式下，多次返回值的均值），比如 `make_averaged(roll_dice)(i, some_dice)` 就是“一次扔 i 个 some_dice” 这种扔法的均值是多少
    ```python
    def make_averaged(original_function, trials_count=1000):
        def evaluate(*arg): # 内层函数接收 *arg 使 original_function 可以运行
            cnt = [None] * trials_count
            for i in range(trials_count):
                cnt[i] = original_function(*arg)
            avg = sum(cnt) / trials_count
            return avg
        return evaluate
    ```

    `winner(strategy0, strategy1)` 对两种策略进行模拟完整 `play()` ，返回胜者 0/1，于是就可以利用 `make_averaged(winner)(strategy0, strategy1)` 来返回 strategy1 对 strategy0 的胜率（因为恰好 strategy1 胜利返回 1 ），反过来先后手的胜率总体平均一下，strategy0 的胜率就是：
    ```
    (   1 - make_averaged(winner)(strategy0, strategy1) + \
            make_averaged(winner)(strategy1, strategy0) ) / 2
    ```

    `more_boar_strategy(score, opponent_score, cutoff=8, num_rolls=6)` 要利用 piggy_point，由于 roll_dice(0) 的结果使可确定的，若发现这样可以触发 more_boar ，则先 piggy_point 多扔一次，或者 piggy_point 高于所期望的 cutoff 值时也选择 piggy_point ，否则默认扔 num_roll 次

    `final_strategy(score, opponent_score)` 分为三个部分：
    * 如果 piggy_point 直接达到 goal 就 roll_dice(0)
    * 如果离 goal 很近的范围，并且对手离自己很远，进入求稳的模式，寻找能使均值大于 5 、且概率满足设定 rate 的最小扔次数
    * 否则正常 more_boar_strategy
