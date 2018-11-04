from random import randint

command = ['up', 'down', 'right', 'left']


def next_step(matrix):
    # matrix里是当前的状态，例如
    # matrix=[[0, 0, 0, 0],
    #         [0, 2, 0, 0],
    #         [0, 0, 1024, 0],
    #         [0, 0, 8, 0]]
    # 就说明相应位置上有相应的数字
    # 然后只需返回字符串格式的命令（command中的那些）就可以进行操作
    # 下面的示例是随机返回
    # 如果注释掉这个函数，就可以手动操作当作普通2048游戏玩
    return command[randint(0, 3)]
