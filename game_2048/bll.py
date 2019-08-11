"""
    逻辑处理模块
    1.0 将核心算法粘贴进来
    2.0 将所有参数，改为成员变量．
    3.0 在空白位置上随机产生新数字．
"""

from game_2048.model import Location
import random

class GameCoreController:
    """
        游戏核心控制器
    """

    def __init__(self):
        # self.__map = [
        #     [0, 0, 0, 0],
        #     [0, 0, 0, 0],
        #     [0, 0, 0, 0],
        #     [0, 0, 0, 0],
        # ]
        self.__map = [
            [0] * 4,
            [0] * 4,
            [0] * 4,
            [0] * 4,
        ]
        # 用于存储去零和合并的列表
        self.__list_merge = []
        # 用于存储空位置的列表
        self.__list_empty_location = []

    @property
    def map(self):
        return self.__map

    def zero_to_end(self):
        for i in range(len(self.__list_merge) - 1, -1, -1):
            if self.__list_merge[i] == 0:
                del self.__list_merge[i]
                self.__list_merge.append(0)

    def merge(self):
        self.zero_to_end()
        for i in range(len(self.__list_merge) - 1):
            if self.__list_merge[i] == self.__list_merge[i + 1]:
                self.__list_merge[i] += self.__list_merge[i + 1]
                self.__list_merge[i + 1] = 0
        self.zero_to_end()

    def move_left(self):
        for r in range(len(self.__map)):
            self.__list_merge[:] = self.__map[r]
            self.merge()
            self.__map[r][:] = self.__list_merge

    def move_right(self):
        for r in range(len(self.__map)):
            self.__list_merge[:] = self.__map[r][::-1]
            self.merge()
            self.__map[r][::-1] = self.__list_merge

    def move_up(self):
        for c in range(4):
            # 清空合并列表，目的：避免之前列表中的结果，对本次有影响．
            self.__list_merge.clear()
            for r in range(4):
                self.__list_merge.append(self.__map[r][c])
            self.merge()
            for r in range(4):
                self.__map[r][c] = self.__list_merge[r]

    def move_down(self):
        for c in range(4):
            self.__list_merge.clear()
            for r in range(3, -1, -1):
                self.__list_merge.append(self.__map[r][c])
            self.merge()
            for r in range(3, -1, -1):
                self.__map[r][c] = self.__list_merge[3 - r]

    def __calculate_empty_location(self):
        self.__list_empty_location.clear()
        for r in range(4):
            for c in range(4):
                if self.__map[r][c] == 0:
                    # 创建位置对象
                    loc = Location(r,c)
                    self.__list_empty_location.append(loc)

    def generate_new_number(self):
        """
            随机生成新数字
        :return:
        """
        self.__calculate_empty_location()
        if len(self.__list_empty_location) ==0:
            return
        # 从空位置列表中，随机选择一个元素．
        loc = random.choice(self.__list_empty_location)
        # 随机生成数字
        self.__map[loc.r_index][loc.c_index] = 4 if random.randint(1,10) == 1 else 2
        # 因为上一行代码已经占了该空位置，所以从空位置列表中移除当前位置．
        self.__list_empty_location.remove(loc)

    def print_map(self):
        print("----------------")
        for r in range(len(self.__map)):
            for c in range(len(self.__map[r])):
                print(self.__map[r][c], end=" ")
            print()



#------------------以下为测试代码---------------------------
def print_map(map):
    print("----------------")
    for r in range(len(map)):
        for c in range(len(map[r])):
            print(map[r][c], end=" ")
        print()


if __name__ == "__main__":
    core = GameCoreController()
    print_map(core.map)
    core.generate_new_number()
    core.generate_new_number()
    print_map(core.map)
