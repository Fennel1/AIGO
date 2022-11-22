'''
@brief: 五子棋ai
@birth: created by 20206521 on 2022-10-20
@version: V1.1.1
@revision: last revised by 20206521 on 2022-11-21
'''

COLUMN = 15
ROW = 15
DEPTH = 1

list_all = []
ans = [0, 0]

go_x = [0, 1, 1, -1]
go_y = [1, 0, 1, 1]

check_shape = [
               (50, (0, 1, 1, 0, 0)),
               (50, (0, 0, 1, 1, 0)),

               (200, (1, 1, 0, 1, 0)),
               (500, (0, 0, 1, 1, 1)),
               (500, (1, 1, 1, 0, 0)),

               (10000, (0, 1, 0, 1, 1, 0)),
               (10000, (0, 1, 1, 0, 1, 0)),
               (10000, (1, 1, 0, 1, 1)),

               (50000, (0, 1, 1, 1, 0)),
               (50000, (1, 1, 1, 0, 1)),
               (50000, (1, 0, 1, 1, 1)),
               
               (90000, (1, 1, 1, 1, 0)),
               (90000, (0, 1, 1, 1, 1)),
               
               (5000000, (0, 1, 1, 1, 1, 0)),
               ]

'''
    功能：α-β剪枝的极大极小搜索
    输入：搜索深度、α、β、当前棋盘状态（我方棋子集合、敌方棋子集合、所有棋子集合）
    输出：α值
'''
def maxmin(depth, alpha, beta, list1, list2, list3):

    if depth == 0:
        return get_score(list1, list2)

    blank_list = list(set(list_all).difference(set(list3)))
    order(blank_list, list3[-1])
    
    for now_step in blank_list:
        if not has_neighbour(now_step, list3):
            continue

        list1.append(now_step)
        list3.append(now_step)
        
        value = -maxmin(depth - 1, -beta, -alpha, list2, list1, list3)
        
        list1.remove(now_step)
        list3.remove(now_step)

        if value > alpha:
            if depth == DEPTH:
                ans[0], ans[1] = now_step[0], now_step[1]
            if value >= beta:
                return beta
            alpha = value

    return alpha

'''
    功能：根据棋盘状态计算分数
    输入：当前棋盘状态（我方棋子集合、敌方棋子集合）
    输出：分数
'''
def get_score(list1, list2):
    my_arr, enemy_arr = [], []
    my_score, enemy_score = 0, 0
    for p in list1:
        for k in range(4):
            my_score += get_score_my(p, k, list2, list1, my_arr, 0)

    
    for p in list2:
        for k in range(4):
            enemy_score += get_score_enemy(p, k, list1, list2, enemy_arr, 50)

    return my_score - enemy_score*0.1

'''
    功能：计算我方棋子在一点处一个方向上的分数
    输入：当前点坐标、方向、当前棋盘状态（我方棋子集合、敌方棋子集合）、当前点已有棋型集合、偏置
    输出：分数
'''
def get_score_my(p, k, enemy_list, my_list, arr, b):
    add_score = 0  
    max_score_shape = (0, None)
    if check_line(p, k, arr):
        return 0

    for offset in range(-5, 1):
        pos = []
        for i in range(0, 6):
            if (p[0] + (i+offset) * go_x[k], p[1] + (i+offset) * go_y[k]) in enemy_list:
                pos.append(2)
            elif (p[0] + (i+offset) * go_x[k], p[1] + (i+offset) * go_y[k]) in my_list:
                pos.append(1)
            elif 0 <= p[0] + (i+offset) * go_x[k] <= ROW and 0 <= p[1] + (i+offset) * go_y[k] <= COLUMN:
                pos.append(0)
            else:
                pos.append(-1)
        shape5 = (pos[0], pos[1], pos[2], pos[3], pos[4])
        shape6 = (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5])

        for (score, shape) in check_shape:
            if shape5 == shape or shape6 == shape:
                if score > max_score_shape[0]:
                    max_score_shape = (score, ( (p[0] + (0+offset) * go_x[k], p[1] + (0+offset) * go_y[k]),
                                                (p[0] + (1+offset) * go_x[k], p[1] + (1+offset) * go_y[k]),
                                                (p[0] + (2+offset) * go_x[k], p[1] + (2+offset) * go_y[k]),
                                                (p[0] + (3+offset) * go_x[k], p[1] + (3+offset) * go_y[k]),
                                                (p[0] + (4+offset) * go_x[k], p[1] + (4+offset) * go_y[k])), (go_x[k], go_y[k]))

    if max_score_shape[1] is not None:
        for item in arr:
            for shape1 in item[1]:
                for shape2 in max_score_shape[1]:
                    if shape1 == shape2:
                        add_score += item[0]*0.5 + max_score_shape[0]
        arr.append(max_score_shape)

    return add_score + max_score_shape[0] + b

'''
    功能：计算敌方棋子在一点处一个方向上的分数
    输入：当前点坐标、方向、当前棋盘状态（我方棋子集合、敌方棋子集合）、当前点已有棋型集合、偏置
    输出：分数
'''
def get_score_enemy(p, k, enemy_list, my_list, arr, b):
    add_score = 0  
    max_score_shape = (0, None)
    if check_line(p, k, arr):
        return 0

    for offset in range(-5, 1):
        pos = []
        for i in range(0, 6):
            if (p[0] + (i+offset) * go_x[k], p[1] + (i+offset) * go_y[k]) in enemy_list:
                pos.append(2)
            elif (p[0] + (i+offset) * go_x[k], p[1] + (i+offset) * go_y[k]) in my_list:
                pos.append(1)
            elif 0 <= p[0] + (i+offset) * go_x[k] <= ROW and 0 <= p[1] + (i+offset) * go_y[k] <= COLUMN:
                pos.append(0)
            else:
                pos.append(-1)
        shape5 = (pos[0], pos[1], pos[2], pos[3], pos[4])
        shape6 = (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5])

        for (score, shape) in check_shape:
            if shape5 == shape or shape6 == shape:
                if score > max_score_shape[0]:
                    max_score_shape = (score, ( (p[0] + (0+offset) * go_x[k], p[1] + (0+offset) * go_y[k]),
                                                (p[0] + (1+offset) * go_x[k], p[1] + (1+offset) * go_y[k]),
                                                (p[0] + (2+offset) * go_x[k], p[1] + (2+offset) * go_y[k]),
                                                (p[0] + (3+offset) * go_x[k], p[1] + (3+offset) * go_y[k]),
                                                (p[0] + (4+offset) * go_x[k], p[1] + (4+offset) * go_y[k])), (go_x[k], go_y[k]))

    if max_score_shape[1] is not None:
        for item in arr:
            for shape1 in item[1]:
                for shape2 in max_score_shape[1]:
                    if shape1 == shape2:
                        add_score += item[0] + max_score_shape[0]
        arr.append(max_score_shape)

    return add_score + max_score_shape[0] + b

'''
    功能：判断我方是否有必胜棋型
    输入：当前棋盘状态（我方棋子集合、敌方棋子集合）
    输出：若有返回点坐标，否则返回None
'''
def check_win(list1, list2):
    for i in range(ROW):
        for j in range(COLUMN):
            if (i, j) not in list1:
                continue
            for k in range(4):
                for offset in range(-5, 1):
                    pos = []
                    for p in range(0, 6):
                        if (i + (p + offset) * go_x[k], j + (p + offset) * go_y[k]) in list2:
                            pos.append(2)
                        elif (i + (p + offset) * go_x[k], j + (p + offset) * go_y[k]) in list1:
                            pos.append(1)
                        elif 0 <= i + (p + offset) * go_x[k] <= ROW and 0 <= j + (p + offset) * go_y[k] <= COLUMN:
                            pos.append(0)
                        else:
                            pos.append(-1)
                    tmp_shape5 = (pos[0], pos[1], pos[2], pos[3], pos[4])
                    if tmp_shape5 == (1,1,1,1,0):
                        return (i + (4 + offset) * go_x[k], j + (4 + offset) * go_y[k])
                    elif tmp_shape5 == (1,1,1,0,1):
                        return (i + (3 + offset) * go_x[k], j + (3 + offset) * go_y[k])
                    elif tmp_shape5 == (1,1,0,1,1):
                        return (i + (2 + offset) * go_x[k], j + (2 + offset) * go_y[k])
                    elif tmp_shape5 == (1,0,1,1,1):
                        return (i + (1 + offset) * go_x[k], j + (1 + offset) * go_y[k])
                    elif tmp_shape5 == (0,1,1,1,1):
                        return (i + (0 + offset) * go_x[k], j + (0 + offset) * go_y[k])
    return None

'''
    功能：判断敌方是否有冲四棋型
    输入：当前棋盘状态（我方棋子集合、敌方棋子集合）
    输出：若有返回点坐标，否则返回None
'''
def check_enemy4(list1, list2):
    for i in range(ROW):
        for j in range(COLUMN):
            if (i, j) not in list2:
                continue
            for k in range(4):
                for offset in range(-5, 1):
                    pos = []
                    for p in range(0, 6):
                        if (i + (p + offset) * go_x[k], j + (p + offset) * go_y[k]) in list2:
                            pos.append(2)
                        elif (i + (p + offset) * go_x[k], j + (p + offset) * go_y[k]) in list1:
                            pos.append(1)
                        elif 0 <= i + (p + offset) * go_x[k] <= ROW and 0 <= j + (p + offset) * go_y[k] <= COLUMN:
                            pos.append(0)
                        else:
                            pos.append(-1)
                    tmp_shape5 = (pos[0], pos[1], pos[2], pos[3], pos[4])
                    tmp_shape6 = (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5])

                    if tmp_shape6 == (0,2,2,2,2,1):
                        return (i + (0+offset) * go_x[k], j + (0+offset) * go_y[k])
                    elif tmp_shape6 == (1,2,2,2,2,0):
                        return (i + (5+offset) * go_x[k], j + (5+offset) * go_y[k])
                    elif tmp_shape5 == (2,0,2,2,2):
                        return (i + (1+offset) * go_x[k], j + (1+offset) * go_y[k])
                    elif tmp_shape5 == (2,2,0,2,2):
                        return (i + (2+offset) * go_x[k], j + (2+offset) * go_y[k])
                    elif tmp_shape5 == (2,2,2,0,2):
                        return (i + (3+offset) * go_x[k], j + (3+offset) * go_y[k])
    return None

'''
    功能：特判下述棋型
            o
            x
            ×o
            ××
                o
    输入：当前棋盘状态（我方棋子集合、敌方棋子集合）
    输出：若满足返回True，否则返回False
'''
def check_staus(listai, listhum):
    if (6, 6) in listhum and (7, 7) in listhum and (8, 8) in listhum and (7, 8) in listhum \
        and (5, 5) in listai and (9, 9) in listai and (8, 7) in listai:
        return True
    return False

'''
    功能：排序可行位置列表
    输入：可行位置列表、最新落子点坐标
'''
def order(blank_list, last_pos):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i == 0 and j == 0) or (last_pos[0] + i, last_pos[1] + j) not in blank_list:
                continue
            else:
                blank_list.remove((last_pos[0] + i, last_pos[1] + j))
                blank_list.insert(0, (last_pos[0] + i, last_pos[1] + j))

'''
    功能：判断当前点周围是否有棋子
    输入：当前点坐标、当前棋盘状态
    输出：若满足返回True，否则返回False
'''
def has_neighbour(pt, list3):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if (pt[0] + i, pt[1] + j) in list3:
                return True
    return False

def check_line(p, k, arr):
    for line in arr:
        for pt in line[1]:
            if p == pt and (go_x[k], go_y[k]) == line[2]:
                return True
    return False
'''
    功能：搜索最优点
    输入：当前棋盘状态（我方棋子集合、敌方棋子集合、所有棋子集合）
    输出：最优点
'''
def ai(listai, listhum, listall):
    # 初始位置或特判棋型
    if len(listai)+len(listhum) == 0:
        return (7, 7)
    if len(listai)+len(listhum) == 1:
        return (8, 7)
    if len(listai)+len(listhum) == 7 and check_staus(listai, listhum):
        return (7, 6)

    # 检查是否有我方五连棋型与敌方四连棋型
    if len(listai) >= 4:
        pos = check_win(listai, listhum)
        if pos != None and pos not in listai:
            return pos
    if len(listhum) >= 4:
        pos = check_enemy4(listai, listhum)
        if pos != None and pos not in listai:
            return pos

    global list_all
    list_all = listall
    list_now = listai + listhum

    # 进入搜索
    maxmin(DEPTH, -10000000, 10000000, listai, listhum, list_now)
    return (ans[0], ans[1])