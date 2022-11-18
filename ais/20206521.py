from math import *
from graphics import *

GRID_WIDTH = 40

COLUMN = 15
ROW = 15

# list1 = []  # AI
# list2 = []  # human
# list3 = []  # all

list_all = []  # 整个棋盘的点

next_point = [0, 0]  # AI下一步最应该下的位置

num_ai = 0
# shape_score = []

ratio = 1  # 进攻的系数   大于1 进攻型，  小于1 防守型
DEPTH = 1  # 搜索深度   只能是单数。  如果是负数， 评估函数评估的的是自己多少步之后的自己得分的最大值，并不意味着是最好的棋， 评估函数的问题


# 棋型的评估分数,表示当棋局为不同形状时的得分
shape_score = [
            #    (20, (0, 1, 0, 1, 0)),
               (50, (0, 1, 1, 0, 0)),
               (50, (0, 0, 1, 1, 0)),
               (200, (1, 1, 0, 1, 0)),
               (500, (0, 0, 1, 1, 1)),
               (500, (1, 1, 1, 0, 0)),
               (50000, (0, 1, 1, 1, 0)),
               (10000, (0, 1, 0, 1, 1, 0)),
               (10000, (0, 1, 1, 0, 1, 0)),
               (50000, (1, 1, 1, 0, 1)),
               (10000, (1, 1, 0, 1, 1)),
               (50000, (1, 0, 1, 1, 1)),
               (90000, (1, 1, 1, 1, 0)),
               (90000, (0, 1, 1, 1, 1)),
               (5000000, (0, 1, 1, 1, 1, 0)),
            #    (99999999, (1, 1, 1, 1, 1))
               ]

shape_score2 = [
#眠二
               (100, (1, 1, 0, 0, 0)),
               (100, (0, 0, 0, 1, 1)),
               (100, (1, 0, 1, 0, 0)),
               (100, (0, 0, 1, 0, 1)),
               (100, (1, 0, 0, 1, 0)),
               (100, (0, 1, 0, 0, 1)),
               (100, (1, 0, 0, 0, 1)),
#活二
               (700, (0, 0, 1, 1, 0, 0)),
               (700, (0, 1, 0, 1, 0)),
               (700, (0, 1, 0, 0, 1, 0)),
#眠三
               (2000, (1, 1, 1, 0, 0)),
               (2000, (0, 0, 1, 1, 1)),
               (2000, (1, 1, 0, 1, 0)),
               (2000, (0, 1, 0, 1, 1)),
               (2000, (1, 0, 1, 1, 0)),
               (2000, (0, 1, 1, 0, 1)),
               (2000, (1, 1, 0, 0, 1)),
               (2000, (1, 0, 0, 1, 1)),
               (2000, (1, 0, 1, 0, 1)),
               (2000, (0, 1, 1, 1, 0)),
#活三
               (30000, (0, 1, 1, 1, 0, 0)),
               (30000, (0, 0, 1, 1, 1, 0)),
               (30000, (0, 1, 1, 0, 1, 0)),
               (30000, (0, 1, 0, 1, 1, 0)),
#冲四
               (50000, (1, 1, 1, 1, 0)),
               (50000, (0, 1, 1, 1, 1)),
               (50000, (1, 1, 1, 0, 1)),
               (50000, (1, 0, 1, 1, 1)),
               (50000, (1, 1, 0, 1, 1)),
#活四
               (100000, (0, 1, 1, 1, 1, 0))]

def ai(listai, listhum, listall):
    if len(listai)+len(listhum) == 0:
        return (7, 7)
    global num_ai
    global shape_score
    if len(listai)+len(listhum) == 1:
        num_ai += 1
        return (8, 7)
    
    if len(listai)+len(listhum) == 7 and check_staus(listai, listhum):
        return (7, 6)

    if len(listai) >= 4:
        pos = check_win(listai, listhum)
        if pos != None and pos not in listai:
            print("AI下的位置：" + str(pos) + "\t剪枝次数：" + str(0) + "\t搜索次数：" + str(0))
            return pos
    if (len(listhum)) >= 4:
        pos = check_enemy4(listai, listhum)
        if pos != None and pos not in listai:
            print("AI下的位置：" + str(pos) + "\t剪枝次数：" + str(0) + "\t搜索次数：" + str(0))
            return pos

    global list_all
    list_all = listall
    list_now = listai + listhum
    global cut_count   # 统计剪枝次数
    cut_count = 0
    global search_count   # 统计搜索次数
    search_count = 0

    # 初始化 负值极大算法
    negamax(True, DEPTH, -99999999, 99999999, listai, listhum, list_now)
    print("AI下的位置：" + str(next_point) + "\t剪枝次数：" + str(cut_count) + "\t搜索次数：" + str(search_count))

    return (next_point[0], next_point[1])


# 负值极大算法搜索 alpha + beta剪枝,合并极大节点和极小节点两种情况,减少代码量
# 在一盘棋局中,若到棋手A走棋,alpha相当于棋手A得到的最好的值,对于棋手A的值,从对手的角度看就要取负值.
def negamax(is_ai, depth, alpha, beta, list1, list2, list3):
    
    # 游戏是否结束 | | 探索的递归深度是否到边界
    # if game_win(list1) or game_win(list2) or depth == 0:
    #     return evaluation(is_ai, list1, list2)

    if depth == 0:
        return evaluation(is_ai, list1, list2)

    # list_all - list3 = {可落子的点集}
    blank_list = list(set(list_all).difference(set(list3)))
    order(blank_list, list3)   # 按搜索顺序排序  提高剪枝效率
    
    # 遍历每一个候选步
    for next_step in blank_list:
        # 如果要评估的位置没有相邻的子， 则不去评估  减少计算
        if not has_neightnor(next_step, list3):
            continue

        global search_count
        search_count += 1

        # 判断是否为ai走棋
        if is_ai:
            list1.append(next_step)
        else:
            list2.append(next_step)
        list3.append(next_step)
        
        # 返回到上一层节点时，会给出分数的相反数(因为返回的值相当于是在对手的选择下对手对当前棋盘的评估分数,而作为他的对立方,要把分数取反)
        # alpha可以视为当前情况下，当前棋手可以得到的最好值，当前棋手得到最好值 == 对手不愿意接受的最差值，因为对手需要不断提高
        value = -negamax(not is_ai, depth - 1, -beta, -alpha, list1, list2, list3)
        
        # 将刚才走棋移除
        if is_ai:
            list1.remove(next_step)
        else:
            list2.remove(next_step)
        list3.remove(next_step)

        if value > alpha:
            # print(str(value) + " [alpha: " + str(alpha) + "beta:" + str(beta) + ']')
            # print(list3)
            # 当depth == DEPTH时,由于在循环内不断迭代,总会在考虑后三步棋的情况下逐渐找到最好的走子方式;
            if depth == DEPTH:
                next_point[0] = next_step[0]
                next_point[1] = next_step[1]
            # alpha + beta剪枝点
            # 当当前value > beta 时相当于 对手的 value< -alpha,对手肯定不会考虑这个选择
            if value >= beta:
                global cut_count
                cut_count += 1
                # 因为当前 depth中 仍需要遍历候选点,return 之后直接返回上层,上层将返回值取负值,因为当调用该函数时alpah -> -beta,必定返回上层迭代时,value < alpha, 达到剪枝目的
                return beta
            alpha = value

    return alpha


#  离最后落子的邻居位置最有可能是最优点
def order(blank_list, list3):
    # list3[-1] 表示 list3 中最后一个落子
    last_pt = list3[-1]
    
    # for item in blank_list:
    # 在最后落子附近搜索是否有可以落子的点
    for i in range(-1, 2):
        for j in range(-1, 2):
            # 当 i = j = 0 是表示最后落子,因为在其附近搜索所以舍弃 i=j=0;
            if i == 0 and j == 0:
                continue
            # 当 最后落子点附近有可选点时,先从删除,然后从候选点列表首部插入
            if (last_pt[0] + i, last_pt[1] + j) in blank_list:
                blank_list.remove((last_pt[0] + i, last_pt[1] + j))
                blank_list.insert(0, (last_pt[0] + i, last_pt[1] + j))

# 判断点 pt 是否有邻居点
def has_neightnor(pt, list3):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if (pt[0] + i, pt[1] + j) in list3:
                return True
    return False


# 评估函数,主要是评估当前棋局的得分
# evaluation 为启发式的评价函数，alpha+beta搜索是相当于在假设双方在同一评价函数函数情况下才有效
def evaluation(is_ai, list1, list2):
    total_score = 0

    # 判断是否为 ai 方
    if is_ai:
        my_list = list1
        enemy_list = list2
    else:
        my_list = list2
        enemy_list = list1

    # 算自己的得分
    score_all_arr = []  # 得分形状的位置 用于计算如果有相交 得分翻倍
    my_score = 0
    for pt in my_list:
        m = pt[0]
        n = pt[1]
        my_score += cal_score_my(m, n, 0, 1, enemy_list, my_list, score_all_arr, 0)
        my_score += cal_score_my(m, n, 1, 0, enemy_list, my_list, score_all_arr, 0)
        my_score += cal_score_my(m, n, 1, 1, enemy_list, my_list, score_all_arr, 0)
        my_score += cal_score_my(m, n, -1, 1, enemy_list, my_list, score_all_arr, 0)

    #  算敌人的得分， 并减去
    score_all_arr_enemy = []
    enemy_score = 0
    for pt in enemy_list:
        m = pt[0]
        n = pt[1]
        enemy_score += cal_score_enemy(m, n, 0, 1, my_list, enemy_list, score_all_arr_enemy, 50)
        enemy_score += cal_score_enemy(m, n, 1, 0, my_list, enemy_list, score_all_arr_enemy, 50)
        enemy_score += cal_score_enemy(m, n, 1, 1, my_list, enemy_list, score_all_arr_enemy, 50)
        enemy_score += cal_score_enemy(m, n, -1, 1, my_list, enemy_list, score_all_arr_enemy, 50)

    # 本方分数 减去 敌方分数
    total_score = my_score - enemy_score*ratio*0.1

    return total_score


# 每个方向上的分值计算
def cal_score_my(m, n, x_decrict, y_derice, enemy_list, my_list, score_all_arr, b):
    add_score = 0  # 加分项
    # 在一个方向上， 只取最大的得分项
    max_score_shape = (0, None)
    # 如果此方向上，该点已经有得分形状，不重复计算
    for item in score_all_arr:
        for pt in item[1]:
            if m == pt[0] and n == pt[1] and x_decrict == item[2][0] and y_derice == item[2][1]:
                return 0

    # 在落子点 左右方向上循环查找得分形状
    for offset in range(-5, 1):
        # offset = -2
        pos = []
        for i in range(0, 6):
            if (m + (i + offset) * x_decrict, n + (i + offset) * y_derice) in enemy_list:
                pos.append(2)
            elif (m + (i + offset) * x_decrict, n + (i + offset) * y_derice) in my_list:
                pos.append(1)
            elif 0 <= m + (i + offset) * x_decrict <= ROW and 0 <= n + (i + offset) * y_derice <= COLUMN:
                pos.append(0)
            else:
                pos.append(-1)
        tmp_shap5 = (pos[0], pos[1], pos[2], pos[3], pos[4])
        tmp_shap6 = (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5])

        for (score, shape) in shape_score:
            if tmp_shap5 == shape or tmp_shap6 == shape:
                # if tmp_shap5 == (1,1,1,1,1):
                    # print('win')
                if score > max_score_shape[0]:
                    max_score_shape = (score, ((m + (0+offset) * x_decrict, n + (0+offset) * y_derice),
                                               (m + (1+offset) * x_decrict, n + (1+offset) * y_derice),
                                               (m + (2+offset) * x_decrict, n + (2+offset) * y_derice),
                                               (m + (3+offset) * x_decrict, n + (3+offset) * y_derice),
                                               (m + (4+offset) * x_decrict, n + (4+offset) * y_derice)), (x_decrict, y_derice))

    # 计算两个形状相交， 如两个3活 相交， 得分增加 一个子的除外
    if max_score_shape[1] is not None:
        for item in score_all_arr:
            for pt1 in item[1]:
                for pt2 in max_score_shape[1]:
                    if pt1 == pt2 and max_score_shape[0] > 10 and item[0] > 10:
                        add_score += item[0]*0.5 + max_score_shape[0]

        score_all_arr.append(max_score_shape)

    return add_score + max_score_shape[0] + b

def cal_score_enemy(m, n, x_decrict, y_derice, enemy_list, my_list, score_all_arr, b):
    add_score = 0  # 加分项
    # 在一个方向上， 只取最大的得分项
    max_score_shape = (0, None)
    # 如果此方向上，该点已经有得分形状，不重复计算
    for item in score_all_arr:
        for pt in item[1]:
            if m == pt[0] and n == pt[1] and x_decrict == item[2][0] and y_derice == item[2][1]:
                return 0

    # 在落子点 左右方向上循环查找得分形状
    for offset in range(-5, 1):
        # offset = -2
        pos = []
        for i in range(0, 6):
            if (m + (i + offset) * x_decrict, n + (i + offset) * y_derice) in enemy_list:
                pos.append(2)
            elif (m + (i + offset) * x_decrict, n + (i + offset) * y_derice) in my_list:
                pos.append(1)
            elif 0 <= m + (i + offset) * x_decrict <= ROW and 0 <= n + (i + offset) * y_derice <= COLUMN:
                pos.append(0)
            else:
                pos.append(-1)
        tmp_shap5 = (pos[0], pos[1], pos[2], pos[3], pos[4])
        tmp_shap6 = (pos[0], pos[1], pos[2], pos[3], pos[4], pos[5])

        for (score, shape) in shape_score:
            if tmp_shap5 == shape or tmp_shap6 == shape:
                # if tmp_shap5 == (1,1,1,1,1):
                    # print('win')
                if score > max_score_shape[0]:
                    max_score_shape = (score, ((m + (0+offset) * x_decrict, n + (0+offset) * y_derice),
                                               (m + (1+offset) * x_decrict, n + (1+offset) * y_derice),
                                               (m + (2+offset) * x_decrict, n + (2+offset) * y_derice),
                                               (m + (3+offset) * x_decrict, n + (3+offset) * y_derice),
                                               (m + (4+offset) * x_decrict, n + (4+offset) * y_derice)), (x_decrict, y_derice))

    # 计算两个形状相交， 如两个3活 相交， 得分增加 一个子的除外
    if max_score_shape[1] is not None:
        for item in score_all_arr:
            for pt1 in item[1]:
                for pt2 in max_score_shape[1]:
                    if pt1 == pt2 and max_score_shape[0] > 10 and item[0] > 10:
                        add_score += item[0] + max_score_shape[0]

        score_all_arr.append(max_score_shape)

    return add_score + max_score_shape[0] + b

go_x = [0,1,1,-1]
go_y = [1,0,1,1]

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


def check_staus(listai, listhum):
    """
    o
     x
      ×o
      ××
        o
    """
    if (6, 6) in listhum and (7, 7) in listhum and (8, 8) in listhum and (7, 8) in listhum \
        and (5, 5) in listai and (9, 9) in listai and (8, 7) in listai:
        return True
    return False
