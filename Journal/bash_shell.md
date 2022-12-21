## Bash Shell 的一些使用

> 由于之前把 Download 文件夹移到 D盘，又删除重建，反复更改地址
> 导致系统自带下载文件夹变成了 C盘 下的 Download_new


1. 用 cd 进入文件夹，mkdir 创建新文件夹
2. 将 lab00.zip 解压缩
3. mv 移动文件，两个路径用空格隔开

```bash
cd ~/Download_new
unzip lab00.zip
mv ~/Download_new/lab00 ~/Desktop/cs61a/lab
```

```shell script
21224@CalciumArgon MINGW64 ~
$ cd ~/Desktop/cs61a

21224@CalciumArgon MINGW64 ~/Desktop/cs61a
$ ls
journal/  lab/  projects/

21224@CalciumArgon MINGW64 ~/Desktop/cs61a
$ cd lab/lab00

21224@CalciumArgon MINGW64 ~/Desktop/cs61a/lab/lab00
$ ls
__pycache__/  lab00.ok  lab00.py  ok  tests/
```

4. 同时 mv 还可以更改文件名
```bash
mv lab LAB
```

5. 运行 ok 格式的试卷，在终端中填写答案
```bash
python ok -u --local
```

也可以单独运行某部分试卷

其中XXXX是试卷的名字，可以 ls 进 tests 文件夹查看XXXX.py文件的名字

（注意在 labXX 文件夹中运行 ok）
```bash
ls tests
python ok -q XXXX -u --local
```

1. 运行 ok 文件以自动检测代码结果（其中 XXXX 是要测试的函数名）

若显示 unlocked 则需要 ```python ok -u --local``` 先检查未解锁的部分

```bash
python ok --local
python ok -q XXXX --local
```

1. lab01中提到的一些（其中的 XXXXX 是 labxx.py 中要测试函数的名字）

The best way to open an interactive terminal to investigate a failing test for question XXXXX in assignment labxx
```bash
python3 ok -q XXXXX -i
```

The best way to look at an environment diagram to investigate a failing test for question XXXXX in assignment labxx
```shell script
python3 ok -q XXXXX --trace
```
