# ----------------------------------------------------------------- #
# A whole 'zoo class' for all animals and foods                     #
# What we have:                                                     #
#   - Food()    name, type, calorie ...                             #
#   - Animal()  name, species, age, food_needed, happiness ...      #
#       - Other specific animals                                    #
#         with additional characteristics                           #
# ----------------------------------------------------------------- #

class Food:
    def __init__(self, name, type, calorie):
        self.name = name
        self.type = type
        self.calorie = calorie

class Animal:
    scientific_name = "Animalia"    # 默认种类
    play_factor = 2
    inteact_adder = 1   # 初始默认 play() 和 interact() 所加 happiness 的程度

    def __init__(self, name, age=0):
        self.name = name
        self.age = age
        self.calorie_needed = 3000  # 以下是一些默认参数
        self.calorie_eaten = 0      # 需要吃多少, 吃了多少, 当前快乐值
        self.happiness = 10

    # 三种基本行为, eat(), play(), interact()
    def eat(self, food: Food):
        self.calorie_eaten += food.calorie
        print("Nom nom yummy" + food.name + "!")
        if self.calorie_eaten > self.calorie_needed:
            self.happiness -= 1
            print("Ugh so full...")

    def play(self, play_time):
        self.happiness += play_time * self.play_factor
        print("Wooo PLAY TIME!")

    def interact(self, other):
        self.happiness += self.inteact_adder
        print("Yay happy time with " + other.name)


# ------------------------------------------------------ #
# Then we can create other specific animals with Animal()
# ------------------------------------------------------ #

class Elephant(Animal):
    scientific_name = "African Elephant"
    # 其他不重新赋值的类变量都保持和 Animal 父类相同

    def __init__(self, name, age=0):
        # 当只想改一部分父类的内容时
        # 先调用父类本身的初始化
        super().__init__(name, age)
        self.calorie_needed = 5000  # 再调整


class Panda(Animal):
    scientific_name = "Giant Panda"
    play_factor = 4
    inteact_adder = -1  # 只自己玩, 拒绝别人来领地

    # 重写方法后, 再运行就不去父类中找了
    def interact(self, other: Animal):
        self.happiness += self.inteact_adder
        print("I'm solitary panda! Go away " + other.name)


class Lion(Animal):
    scientific_name = "Lion"

    def __init__(self, name, age=0):
        super().__init__(name, age)
        if self.age <= 2:
            self.calorie_needed = 1000
        elif self.age <= 5:
            self.calorie_needed = 2000
        # age > 5 对应默认 3000

    def eat(self, food: Food):
        if food.type == "meat":
            super().eat(food)
            # super() 自动去该类定义时括号里的父类去找
            # 等价于:
            # Animal.eat(self, food)    # 这样更快, 但依赖已知父类名称
        else:
            print("Ewww yucky " + food.name)
            self.happiness -= 1

# ----------------------------------------------------------- #
# 多层抽象, Animal -> Herbivore & Carnivore -> specific animals
# ----------------------------------------------------------- #
class Herbivore(Animal):
    def eat(self, food: Food):
        if food.type == "meat":
            print("Ewww yucky " + food.name)
            self.happiness -= 1
        else:
            super().eat(food)

class Carnivore(Animal):
    def eat(self, food: Food):
        if food.type == "meat":
            super().eat(food)
        else:
            print("Ewww yucky " + food.name)
            self.happiness -= 1

class Snake(Carnivore):
    pass

class Human(Herbivore, Carnivore):
    pass



if __name__ == "__main__":
    lion = Lion("Scar")
    snake = Snake("Sisi")

    print(Food.__bases__, "\n")

    print(lion.__class__)
    print(lion.__class__.__bases__)
    print(lion.__class__.__bases__[0].__bases__)
    print(lion.__class__.__bases__[0].__bases__[0].__bases__, "\n")

    print(snake.__class__)
    print(snake.__class__.__base__)
    print(snake.__class__.__bases__)
    print(snake.__class__.__bases__[0].__bases__)
    print(snake.__class__.__bases__[0].__bases__[0].__bases__, "\n")

    print(Human.__bases__, "\n")

