import os
import time
import importlib
from func_timeout import func_timeout, FunctionTimedOut
from graphics import *

DRAW = True

GRID_WIDTH = 40

COLUMN = 15
ROW = 15

def game_win(list):
    for m in range(COLUMN):
        for n in range(ROW):
            # 判赢条件 ：横,竖,左斜,右斜 共四个方向，若连子为5则判赢；
            if n < ROW - 4 and (m, n) in list and (m, n + 1) in list and (m, n + 2) in list and (m, n + 3) in list and (m, n + 4) in list:
                return True
            elif m < ROW - 4 and (m, n) in list and (m + 1, n) in list and (m + 2, n) in list and (m + 3, n) in list and (m + 4, n) in list:
                return True
            elif m < ROW - 4 and n < ROW - 4 and (m, n) in list and (m + 1, n + 1) in list and (m + 2, n + 2) in list and (m + 3, n + 3) in list and (m + 4, n + 4) in list:
                return True
            elif m < ROW - 4 and n > 3 and (m, n) in list and (m + 1, n - 1) in list and (m + 2, n - 2) in list and (m + 3, n - 3) in list and (m + 4, n - 4) in list:
                return True
    return False

# 实际对局函数
def runChess(game_nos,time_limits,MAX_TIME=360):
        """
        输入： 对局 双方学号
        输出 : 对局结果以及中间过程, result = {'white':xxx ,
                                             'black':xxx,
                                             'winStu':xxx,
                                             'start_time':xxx,
                                             'end_time':xxx,
                                             'steps':[],
                                             'time_by_step':[],
                                             'OutOFMAXTIME':True,
                                             'OUTOFKERNELTIME':True} 
        处理过程: 
            1. 根据学号 导入模块
            2. 生成 对战中全局变量
            3. 记录中间结果
            4. 超时记录
        """

        if DRAW:
            win = gobangwin()

        result = {}
        result['white'] = game_nos[0]
        result['black'] = game_nos[1]
        
        # 生成全局变量
        list_white = []  # AI_WHITE
        list_black = []  # AI_BLACK
        list_summary = []  # all
        steps_times = []
        list_all = []
        out_time_White = 0
        out_time_Black = 0
        for i in range(COLUMN+1):
            for j in range(ROW+1):
                list_all.append((i, j))
                
        change = 0
        g = 0
        m = 0
        n = 0
        steps_times_white = 0
        # 动态引入模块
        ai_white = importlib.import_module('ais.'+ game_nos[0]).ai
        ai_black = importlib.import_module('ais.'+ game_nos[1]).ai
        result['start_time'] = time.time()
        result['WinSituation'] = 'StrengthRolling'

        while g == 0:
                step_start = time.time()
                blank_list = list(set(list_all).difference(set(list_summary)))
                try:
                        pos = blank_list[0]
                        if change % 2 == 0:
                                steps_times_white -= time.time()
                                pos = func_timeout(MAX_TIME, ai_white, args=(list_white, list_black, list_all))
                                steps_times_white += time.time()
                                list_white.append(pos)
                                list_summary.append(pos)
                                if DRAW:
                                    piece = Circle(Point(GRID_WIDTH * pos[0], GRID_WIDTH * pos[1]), 16)
                                    piece.setFill('white')
                                    piece.draw(win)
                                    message = Text(Point(GRID_WIDTH * pos[0], GRID_WIDTH * pos[1]), change+1)
                                    message.setTextColor('black')
                                    message.draw(win)
                        else:
                                pos = func_timeout(MAX_TIME, ai_black, args=(list_black, list_white, list_all))
                                list_black.append(pos)
                                list_summary.append(pos)
                                if DRAW:
                                    piece = Circle(Point(GRID_WIDTH * pos[0], GRID_WIDTH * pos[1]), 16)
                                    piece.setFill('black')
                                    piece.draw(win)
                                    message = Text(Point(GRID_WIDTH * pos[0], GRID_WIDTH * pos[1]), change+1)
                                    message.setTextColor('white')
                                    message.draw(win)
                        if pos not in blank_list:
                                raise ZeroDivisionError
                except FunctionTimedOut:
                        print('[{}FunctionTimedOut] WINER={}'.format(result['white'] if change % 2 == 0 else result['black'],result['white'] if change % 2 != 0 else result['black']))
                        g = 1 
                        result['win_Stu'] = result['white'] if change % 2 != 0 else result['black']
                        result['WinSituation'] = 'OUTOFTIME'
                except ZeroDivisionError:
                        print('[PosInvaild]')
                        if DRAW:
                            message = Text(Point(200, 200), "不可用的位置" + str(pos[0]) + "," + str(pos[1]))
                            message.draw(win)
                        g = 1
                        result['win_Stu'] = result['white'] if change % 2 != 0 else result['black']
                        result['WinSituation'] = 'PosInvaild'
                except BaseException:
                        print('[BaseException]')
                        g = 1
                        result['win_Stu'] = result['white'] if change % 2 != 0 else result['black']        
                        result['WinSituation'] = 'BaseException'

                step_end = time.time()
                step_spend = step_end - step_start
                # 记录 一步 时间
                steps_times.append(step_spend)
                if step_spend > time_limits:
                        if change % 2 == 0:
                                out_time_White += 1
                        else:
                                out_time_Black += 1
                if out_time_Black > 2 or out_time_White > 2 or game_win(list_white) or game_win(list_black) or len(list_summary) == len(list_all):
                        print('game over')
                        if out_time_Black > 2 or game_win(list_white):
                                result['win_Stu'] = result['white']
                        elif out_time_White > 2 or game_win(list_black):
                                result['win_Stu'] = result['black']
                        elif len(list_summary) == len(list_all):
                                result['win_Stu'] = 'NOONE'
                        g = 1

                change += 1
        if DRAW:
            message = Text(Point(100, 120), "Click anywhere to quit.")
            message.draw(win)
            win.getMouse()
            win.close()

        result['end_time'] = time.time()
        result['steps'] = list_summary
        return (result, steps_times_white)

def gobangwin():
    win = GraphWin("this is a gobang game", GRID_WIDTH * COLUMN, GRID_WIDTH * ROW)
    win.setBackground("yellow")
    
    # i1 i2 分别绘制棋盘纵横线
    i1 = 0
    while i1 <= GRID_WIDTH * COLUMN:
        l = Line(Point(i1, 0), Point(i1, GRID_WIDTH * COLUMN))
        l.draw(win)
        i1 = i1 + GRID_WIDTH
    i2 = 0
    while i2 <= GRID_WIDTH * ROW:
        l = Line(Point(0, i2), Point(GRID_WIDTH * ROW, i2))
        l.draw(win)
        i2 = i2 + GRID_WIDTH
    return win

if __name__ == "__main__":
        time_white_total = 0
        result, time_white = runChess(('20206521','ai_1'),1000)
        time_white_total += time_white
        print(time_white_total)
        result["step_total_white"] = time_white_total
        print(result)

        time_white_total = 0
        result, time_white = runChess(('20206521','ai_2'),1000)
        time_white_total += time_white
        print(time_white_total)
        result["step_total_white"] = time_white_total
        print(result)

        time_white_total = 0
        result, time_white = runChess(('20206521','ai_3'),1000)
        time_white_total += time_white
        print(time_white_total)
        result["step_total_white"] = time_white_total
        print(result)

        time_white_total = 0
        result, time_white = runChess(('20206521','ai_4'),1000)
        time_white_total += time_white
        print(time_white_total)
        result["step_total_white"] = time_white_total
        print(result)

        time_white_total = 0
        result, time_white = runChess(('20206521','ai_5'),1000)
        time_white_total += time_white
        print(time_white_total)
        result["step_total_white"] = time_white_total
        print(result)

        time_white_total = 0
        result, time_white = runChess(('20206521','ai_6'),1000)
        time_white_total += time_white
        print(time_white_total)
        result["step_total_white"] = time_white_total
        print(result)

        time_white_total = 0
        result, time_white = runChess(('20206521','ai_7'),1000)
        time_white_total += time_white
        print(time_white_total)
        result["step_total_white"] = time_white_total
        print(result)
