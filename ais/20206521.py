COLUMN = 15
ROW = 15
DEPTH = 1

list_all = []
next_point = [0, 0]

go_x = [0, 1, 1, -1]
go_y = [1, 0, 1, 1]

shape_score = [
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
               ]

def ai(listai, listhum, listall):
    if len(listai)+len(listhum) == 0:
        return (7, 7)
    if len(listai)+len(listhum) == 1:
        return (8, 7)
    
    if len(listai)+len(listhum) == 7 and check_staus(listai, listhum):
        return (7, 6)

    if len(listai) >= 4:
        pos = check_win(listai, listhum)
        if pos != None and pos not in listai:
            # print("AI下的位置：" + str(pos) + "\t剪枝次数：" + str(0) + "\t搜索次数：" + str(0))
            return pos
    if (len(listhum)) >= 4:
        pos = check_enemy4(listai, listhum)
        if pos != None and pos not in listai:
            # print("AI下的位置：" + str(pos) + "\t剪枝次数：" + str(0) + "\t搜索次数：" + str(0))
            return pos

    global list_all
    list_all = listall
    list_now = listai + listhum
    
    global cut_count  
    global search_count   
    cut_count = 0
    search_count = 0

    maxmin(True, DEPTH, -99999999, 99999999, listai, listhum, list_now)
    # print("AI下的位置：" + str(next_point) + "\t剪枝次数：" + str(cut_count) + "\t搜索次数：" + str(search_count))

    return (next_point[0], next_point[1])


def maxmin(is_ai, depth, alpha, beta, list1, list2, list3):

    if depth == 0:
        return evaluation(is_ai, list1, list2)

    blank_list = list(set(list_all).difference(set(list3)))
    order(blank_list, list3) 
    
    for next_step in blank_list:
        if not has_neightnor(next_step, list3):
            continue

        global search_count
        search_count += 1

        if is_ai:
            list1.append(next_step)
        else:
            list2.append(next_step)
        list3.append(next_step)
        
        value = -maxmin(not is_ai, depth - 1, -beta, -alpha, list1, list2, list3)
        
        if is_ai:
            list1.remove(next_step)
        else:
            list2.remove(next_step)
        list3.remove(next_step)

        if value > alpha:
            if depth == DEPTH:
                next_point[0] = next_step[0]
                next_point[1] = next_step[1]
            if value >= beta:
                global cut_count
                cut_count += 1
                return beta
            alpha = value

    return alpha


def order(blank_list, list3):
    last_pt = list3[-1]
    
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if (last_pt[0] + i, last_pt[1] + j) in blank_list:
                blank_list.remove((last_pt[0] + i, last_pt[1] + j))
                blank_list.insert(0, (last_pt[0] + i, last_pt[1] + j))


def has_neightnor(pt, list3):
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            if (pt[0] + i, pt[1] + j) in list3:
                return True
    return False


def evaluation(is_ai, list1, list2):
    if is_ai:
        my_list = list1
        enemy_list = list2
    else:
        my_list = list2
        enemy_list = list1

    score_all_arr = []  
    my_score = 0
    for p in my_list:
        for k in range(4):
            my_score += cal_score_my(p[0], p[1], go_x[k], go_y[k], enemy_list, my_list, score_all_arr, 0)

    score_all_arr_enemy = []
    enemy_score = 0
    for p in enemy_list:
        for k in range(4):
            enemy_score += cal_score_enemy(p[0], p[1], go_x[k], go_y[k], my_list, enemy_list, score_all_arr_enemy, 50)

    return my_score - enemy_score*0.1


def cal_score_my(m, n, x_decrict, y_derice, enemy_list, my_list, score_all_arr, b):
    add_score = 0  
    max_score_shape = (0, None)
    for item in score_all_arr:
        for pt in item[1]:
            if m == pt[0] and n == pt[1] and x_decrict == item[2][0] and y_derice == item[2][1]:
                return 0

    for offset in range(-5, 1):
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
                if score > max_score_shape[0]:
                    max_score_shape = (score, ((m + (0+offset) * x_decrict, n + (0+offset) * y_derice),
                                               (m + (1+offset) * x_decrict, n + (1+offset) * y_derice),
                                               (m + (2+offset) * x_decrict, n + (2+offset) * y_derice),
                                               (m + (3+offset) * x_decrict, n + (3+offset) * y_derice),
                                               (m + (4+offset) * x_decrict, n + (4+offset) * y_derice)), (x_decrict, y_derice))

    if max_score_shape[1] is not None:
        for item in score_all_arr:
            for pt1 in item[1]:
                for pt2 in max_score_shape[1]:
                    if pt1 == pt2 and max_score_shape[0] > 10 and item[0] > 10:
                        add_score += item[0]*0.5 + max_score_shape[0]
        score_all_arr.append(max_score_shape)

    return add_score + max_score_shape[0] + b

def cal_score_enemy(m, n, x_decrict, y_derice, enemy_list, my_list, score_all_arr, b):
    add_score = 0 
    max_score_shape = (0, None)
    for item in score_all_arr:
        for pt in item[1]:
            if m == pt[0] and n == pt[1] and x_decrict == item[2][0] and y_derice == item[2][1]:
                return 0

    for offset in range(-5, 1):
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
                if score > max_score_shape[0]:
                    max_score_shape = (score, ((m + (0+offset) * x_decrict, n + (0+offset) * y_derice),
                                               (m + (1+offset) * x_decrict, n + (1+offset) * y_derice),
                                               (m + (2+offset) * x_decrict, n + (2+offset) * y_derice),
                                               (m + (3+offset) * x_decrict, n + (3+offset) * y_derice),
                                               (m + (4+offset) * x_decrict, n + (4+offset) * y_derice)), (x_decrict, y_derice))

    if max_score_shape[1] is not None:
        for item in score_all_arr:
            for pt1 in item[1]:
                for pt2 in max_score_shape[1]:
                    if pt1 == pt2 and max_score_shape[0] > 10 and item[0] > 10:
                        add_score += item[0] + max_score_shape[0]
        score_all_arr.append(max_score_shape)

    return add_score + max_score_shape[0] + b

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
