from tkinter import *
from logic import *
from random import *
import threading
from copy import deepcopy
from time import sleep
from tkinter.messagebox import showerror, showinfo
import os

SIZE = 500
GRID_LEN = 4
GRID_PADDING = 10

BACKGROUND_COLOR_GAME = "#92877d"
BACKGROUND_COLOR_CELL_EMPTY = "#9e948a"
BACKGROUND_COLOR_DICT = {2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563", \
                         32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61", \
                         512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"}
CELL_COLOR_DICT = {2: "#776e65", 4: "#776e65", 8: "#f9f6f2", 16: "#f9f6f2", \
                   32: "#f9f6f2", 64: "#f9f6f2", 128: "#f9f6f2", 256: "#f9f6f2", \
                   512: "#f9f6f2", 1024: "#f9f6f2", 2048: "#f9f6f2"}
FONT = ("Verdana", 40, "bold")

KEY_UP_ALT = "\'\\uf700\'"
KEY_DOWN_ALT = "\'\\uf701\'"
KEY_LEFT_ALT = "\'\\uf702\'"
KEY_RIGHT_ALT = "\'\\uf703\'"

KEY_UP = "'w'"
KEY_DOWN = "'s'"
KEY_LEFT = "'a'"
KEY_RIGHT = "'d'"


def show_error(e):
    showerror("注意", "请检查next_step函数后继续\n报错信息:\n" + str(e))
    os._exit(1)


class GameGrid(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.auto = False
        try:
            from main import next_step
            self.next_step = next_step
            self.auto = True
        except (ModuleNotFoundError, ImportError):
            showinfo('提示', '未发现对应函数，现在进入手动模式\n使用W,A,S,D控制')

        except Exception as e:
            show_error(e)

        self.grid()
        self.matrix = None
        self.master.title('2048')

        # self.gamelogic = gamelogic
        self.commands = {KEY_UP: up, KEY_DOWN: down, KEY_LEFT: left, KEY_RIGHT: right,
                         KEY_UP_ALT: up, KEY_DOWN_ALT: down, KEY_LEFT_ALT: left, KEY_RIGHT_ALT: right}
        self.commands_auto = {'up': up, 'down': down, 'left': left, 'right': right}
        self.grid_cells = []
        self.init_grid()
        self.init_matrix()
        self.update_grid_cells()

        if not self.auto:
            self.master.bind("<Key>", self.key_down)
        else:
            self.pause_flag = True
            self.pause_button = Button(self, text='开始', command=self.pause)
            self.pause_button.pack(side=LEFT)
            Button(self, text='步进', command=self.one_step).pack(side=LEFT)
            self.scale = Scale(self, from_=1, to=100, orient=HORIZONTAL)
            self.scale.pack(fill=X)
            self.scale.set(1)
            self.thread = threading.Thread(target=self.run)
            self.thread.setDaemon(True)
            self.thread.start()
        self.mainloop()

    def init_grid(self):
        background = Frame(self, bg=BACKGROUND_COLOR_GAME, width=SIZE, height=SIZE)
        background.pack()
        for i in range(GRID_LEN):
            grid_row = []
            for j in range(GRID_LEN):
                cell = Frame(background, bg=BACKGROUND_COLOR_CELL_EMPTY, width=SIZE / GRID_LEN, height=SIZE / GRID_LEN)
                cell.grid(row=i, column=j, padx=GRID_PADDING, pady=GRID_PADDING)
                # font = Font(size=FONT_SIZE, family=FONT_FAMILY, weight=FONT_WEIGHT)
                t = Label(master=cell, text="", bg=BACKGROUND_COLOR_CELL_EMPTY, justify=CENTER, font=FONT, width=4,
                          height=2)
                t.grid()
                grid_row.append(t)

            self.grid_cells.append(grid_row)

    def gen(self):
        return randint(0, GRID_LEN - 1)

    def init_matrix(self):
        self.matrix = new_game(4)

        self.matrix = add_two(self.matrix)
        self.matrix = add_two(self.matrix)

    def update_grid_cells(self):
        for i in range(GRID_LEN):
            for j in range(GRID_LEN):
                new_number = self.matrix[i][j]
                if new_number == 0:
                    self.grid_cells[i][j].configure(text="", bg=BACKGROUND_COLOR_CELL_EMPTY)
                else:
                    self.grid_cells[i][j].configure(text=str(new_number), bg=BACKGROUND_COLOR_DICT[new_number],
                                                    fg=CELL_COLOR_DICT[new_number])
        self.update_idletasks()

    def key_down(self, event):
        key = repr(event.char)
        if key in self.commands:
            self.matrix, done = self.commands[repr(event.char)](self.matrix)
            if done:
                self.matrix = add_two(self.matrix)
                self.update_grid_cells()
                done = False
                if game_state(self.matrix) == 'win':
                    self.grid_cells[1][1].configure(text="You", bg=BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Win!", bg=BACKGROUND_COLOR_CELL_EMPTY)
                if game_state(self.matrix) == 'lose':
                    self.grid_cells[1][1].configure(text="You", bg=BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Lose!", bg=BACKGROUND_COLOR_CELL_EMPTY)

    def generate_next(self):
        index = (self.gen(), self.gen())
        while self.matrix[index[0]][index[1]] != 0:
            index = (self.gen(), self.gen())
        self.matrix[index[0]][index[1]] = 2

    def run(self):
        while not self.pause_flag:
            self.one_step()
            if not self.scale.get() > 95:
                sleep(1 / self.scale.get())

    def pause(self):
        if self.pause_button['text'] == '暂停':
            self.pause_button['text'] = '继续'
            self.pause_flag = True
        elif self.pause_button['text'] == '重新开始':
            del self.matrix
            self.init_matrix()
            self.update_grid_cells()
            self.pause_button['text'] = '开始'
            self.pause_flag = True
        else:
            self.pause_button['text'] = '暂停'
            self.pause_flag = False
            self.thread = threading.Thread(target=self.run)
            self.thread.setDaemon(True)
            self.thread.start()

    def one_step(self):
        key = None
        try:
            key = self.next_step(deepcopy(self.matrix))
            if key not in self.commands_auto:
                show_error('请检查函数返回值！')
        except Exception as e:
            show_error(e)
        if key in self.commands_auto:
            self.matrix, done = self.commands_auto[key](self.matrix)
            if done:
                self.matrix = add_two(self.matrix)
                self.update_grid_cells()
                done = False
                if game_state(self.matrix) == 'win':
                    self.grid_cells[1][1].configure(text="You", bg=BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Win!", bg=BACKGROUND_COLOR_CELL_EMPTY)
                    self.pause_button['text'] = '重新开始'
                if game_state(self.matrix) == 'lose':
                    self.grid_cells[1][1].configure(text="You", bg=BACKGROUND_COLOR_CELL_EMPTY)
                    self.grid_cells[1][2].configure(text="Lose!", bg=BACKGROUND_COLOR_CELL_EMPTY)
                    self.pause_button['text'] = '重新开始'


gamegrid = GameGrid()
# for i in range(10000000):
#     print('asd')
