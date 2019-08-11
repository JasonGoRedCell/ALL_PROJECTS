
from game_2048.bll import GameCoreController
class GameCoreView:
    """
        界面视图类
    """
    def __init__(self):
        self.__manager = GameCoreController()

    def __map_view(self):
        self.__manager.generate_new_number()
        self.__manager.generate_new_number()
        self.__manager.print_map()
        self.__operation_manual()
        self.__operation_list()

    def __display_menu(self):
        """
            显示菜单
        :return:
        """
        print("1) 开始游戏")
        print("2) 退出")

    def __select_menu(self):
        """
        选择菜单
        :return:
        """
        number = input("请输入选项:")
        if number == "1":
            self.__map_view()
        else:
            return

    def __operation_manual(self):
        print("-----------")
        print("游戏操作如下：")
        print("w,上移")
        print("a,左移")
        print("s,下移")
        print("d,右移")

    def __operation_list(self):
        while True:
            number = input("请输入选项:")
            if number == "w":
                self.__manager.move_up()
                self.__manager.generate_new_number()
                self.__manager.print_map()
            elif number == "a":
                self.__manager.move_left()
                self.__manager.generate_new_number()
                self.__manager.print_map()
            elif number == "s":
                self.__manager.move_down()
                self.__manager.generate_new_number()
                self.__manager.print_map()
            elif number == "d":
                self.__manager.move_right()
                self.__manager.generate_new_number()
                self.__manager.print_map()
            elif number =="q":
                break


    def main(self):
        view = GameCoreView()
        view.__display_menu()
        view.__select_menu()

# --------------------------------------------------------
t01 = GameCoreView()
t01.main()
