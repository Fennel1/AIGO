COLUMN = 15
ROW = 15
SIMU_DEEPTH = 4     #模拟总步数

shape_score = {(0, 1, 1, 0, 0):50,
               (0, 0, 1, 1, 0):50,
               (1, 1, 0, 1, 0):200,
               (0, 0, 1, 1, 1):500,
               (1, 1, 1, 0, 0):500,
               (0, 1, 1, 1, 0):5000,
               (0, 1, 0, 1, 1, 0):5000,
               (0, 1, 1, 0, 1, 0):5000,
               (1, 1, 1, 0, 1):5000,
               (1, 1, 0, 1, 1):5000,
               (1, 0, 1, 1, 1):5000,
               (1, 1, 1, 1, 0):5000,
               (0, 1, 1, 1, 1):5000,
               (0, 1, 1, 1, 1, 0):50000,
               (1, 1, 1, 1, 1):99999999}


def ai(listAI, listHuman, listAll):
    ##print(listHuman,"\n")
    if len(listHuman)== 0:
        return 7,7
    elif len(listAI)==0:
        pos = listHuman[0]
        if pos[0] < 15:
            return pos[0]+1,pos[1]
        elif pos[1]<15:
            return pos[0], pos[1] + 1
        else:
            return pos[0]-1,pos[0]-1

    list_AI = listAI.copy()
    list_Human = listHuman.copy()
    list_All = listAll.copy()
    
    pos = get_finally_pos(list_AI, list_Human, list_All)
    # print("finally:",pos)
    #print("f:",listAI,listHuman,"\n\n")
    return pos[0], pos[1]

def get_finally_pos(listAI, listHuman, listAll):
    pos,_,_ = get_pos(True, SIMU_DEEPTH, listAI, listHuman, listAll)
    return pos

def get_pos(IsAI, deepth ,listAI, listHuman, listAll):
    #  #print("游戏者：",IsAI,"层数",deepth-1)
    deepth = deepth - 1

    first_score = get_score(listAI, listHuman, listAll)
    first_other_score = get_score(listHuman, listAI, listAll)
    pos_list = []
    #  #print("fs:",first_score)
    # 对于对方有三连以上，我方没有的情况，加快算法速度
    if first_score < 10000 and first_other_score > 10000:  
        listAI_copy = listAI.copy()
        listHuman_copy = listHuman.copy()
        list_four,ok = check_four(listHuman_copy, listAI_copy) 

        listAI_copy.clear()
        listHuman_copy.clear()
        listAI_copy = listAI.copy()
        listHuman_copy = listHuman.copy()
        list_four2,ok = check_four(listAI_copy, listHuman_copy) 
        #  #print("第二个：", list_four2)
        pos_list = list_four+list_four2
    else:
        #其他情况，正常找六个点即可
        posible_list = find_posible(listHuman,listAI)
        pos_list = get_pos_list(posible_list,listHuman,listAI, listAll, 1.2)
    
    # 找出所有可能的下一步成五个点的，将其置于最前，加快算法运行时间
    list_five = check_five(listAI, listHuman)
    for pos in list_five:
        pos_list.insert(0, pos)

    pos_list = sorted(set(pos_list), key=pos_list.index)

    
    for pos in pos_list:
        listAI.append(pos)
        if game_win(listAI):
            listAI.pop()
            if IsAI:
                #  #print(1,"AI赢")
                return pos,deepth,True
            else:
                #  #print(2,"他赢")
                return pos,deepth, False
        else:
            listAI.pop()
    
    for pos in pos_list:
        list_ai = listAI.copy()
        list_human = listHuman.copy()
        list_ai.append(pos)
        if game_win(list_ai) :
            #  #print("post",pos)
            if IsAI:
                #  #print(3,"AI赢2")
                return pos,deepth, True
            else:
                #  #print(4,"他赢2")
                return pos,deepth,False
        if deepth == 0:
            return pos, deepth,True
        _,re_deepth, ok = get_pos(not IsAI, deepth, list_human, list_ai, listAll)
        if IsAI and ok == True :
            #  #print("完成一次函数调用")
            #  #print(6)
            return pos,deepth,True
        if not IsAI and ok == False:
            #  #print("反方向完成一次函数调用")
            return _,_,False
    
    if deepth != SIMU_DEEPTH-1 and IsAI:
        #  #print("遍历所有返回")
        return pos_list[0],deepth,False
    return pos_list[0],deepth,True    





def get_pos_list(posible_list, listHuman, listAI, listAll,rate = 1):
    base_score = get_score(listAI, listHuman, listAll)
    base_other_score = get_score(listHuman, listAI, listAll)
    # ## #print("b_s:",base_score,"b_o_s:",base_other_score)
    score_list = []
    for pos in posible_list:
        listAI.append(pos)
        score = get_score(listAI, listHuman, listAll)
        other = get_score(listHuman, listAI, listAll)
        score = score - base_score
        other = other - base_other_score
        if score > 10000 and other<-500:
            score += 500
        score = score - other* rate
        score_list.append((score, pos))
        listAI.pop()
    sort_score = sorted(score_list,reverse=True)
    pos_list = []
    for i in range(0, 6):
        if i > len(sort_score):
            break
        pos_list.append(sort_score[i][1])
    # #print("pos_list:",pos_list)
    return pos_list




def check_four(listHuman,listAI):
    pos_list = find_posible(listHuman, listAI, 3)
    return_list = []
    for pos in pos_list:
        listHuman.append(pos)
        # ##print("pos:",pos)
        
        count = 0
        for i in range(-3,4):
            if check_pos((pos[0]+i,pos[1])) and (pos[0]+i,pos[1]) in listHuman:
                ###print("+ 0","pos:",pos,"count:",count,(pos[0]+i,pos[1]))
                count = count + 1
                if count > 3 :
                    return_list.append(pos)
            else:
                count = 0
        count = 0
        for i in range(-3,4):
            if check_pos((pos[0]+i,pos[1]+i)) and (pos[0]+i,pos[1]+i) in listHuman:
                #if pos == (10, 11):
                    #  #print("0 +","pos:",pos,"count:",count,(pos[0]+i,pos[1]+i))
                count = count + 1
                if count > 3:
                    return_list.append(pos)
                    
            else:
                count = 0
        count = 0
        for i in range(-3,4):
            if check_pos((pos[0]+i,pos[1]-i)) and (pos[0]+i,pos[1]-i) in listHuman:
                ###print("+ -","pos:",pos,"count:",count,(pos[0]+i,pos[1]-i))
                count = count + 1
                if count > 3:
                    return_list.append(pos)
            else:
                count = 0
        count = 0
        for i in range(-3,4):
            if check_pos((pos[0],pos[1])) and (pos[0],pos[1]+i) in listHuman:
                ###print("+ +","pos:",pos,"count:",count,(pos[0],pos[1]+i))
                count = count + 1
                if count > 3:
                    return_list.append(pos)
            else:
                count = 0
        listHuman.pop()
    if len(return_list) == 0:
        return return_list, False
    else:
        return  return_list,True

def check_five(check_list, other_list):
    check_list_copy = check_list.copy()
    other_list_copy = other_list.copy()
    posi_list = find_posible(check_list, other_list)
    posi_list2 = find_posible(other_list, check_list)
    return_list = []
    for pos in posi_list:
        check_list_copy.append(pos)
        if game_win(check_list_copy):
            return_list.append(pos)
        check_list_copy.pop()
    for pos in posi_list2:
        other_list_copy.append(pos)
        if game_win(other_list_copy):
            return_list.append(pos)
        other_list_copy.pop()
    
    #  #print("return_list:",return_list)

    return return_list
    

def get_score(check_list,other_list,listAll):
    score = 0
    for pos in check_list:
        score += get_pos_score(1, 0, pos, check_list, other_list, listAll);
        score += get_pos_score(-1, 0, pos, check_list, other_list, listAll);
        score += get_pos_score(0, 1, pos, check_list, other_list, listAll);
        score += get_pos_score(0, -1, pos, check_list, other_list, listAll);
        score += get_pos_score(1, 1, pos, check_list, other_list, listAll);
        score += get_pos_score(-1, 1, pos, check_list, other_list, listAll);
        score += get_pos_score(1, -1, pos, check_list, other_list, listAll);
        score += get_pos_score(-1, -1, pos, check_list, other_list, listAll);
    return score

def get_pos_score(left, right, pos, check_list, other_list, listAll):
    score = 0
    score_pos_tem = []
    for i in range(-1, 5): #这里还没有检查越界情况
        j = left * i
        k = right * i
        if (pos[0] + j, pos[1] + k) in check_list :
            score_pos_tem.append(1)
        elif (pos[0] + j, pos[1]+ k) in other_list:
            score_pos_tem.append(2)
        elif (pos[0] + j, pos[1] + k) in listAll:
            score_pos_tem.append(0)
        else:
            score_pos_tem.append(-1)
    score_pos5 = (score_pos_tem[0],score_pos_tem[1],score_pos_tem[2],score_pos_tem[3],score_pos_tem[4])
    score_pos6 = (score_pos_tem[0],score_pos_tem[1],score_pos_tem[2],score_pos_tem[3],score_pos_tem[4],score_pos_tem[5])
    # if(pos == (10, 9) ):
    #     ##print("ps:",pos,check_list)
    #     ##print(score_pos5)
    #     ##print(score_pos6)
    #     ##print(shape_score.get(score_pos5))
    if shape_score.get(score_pos5)!=None:
        score += shape_score[score_pos5]
    if shape_score.get(score_pos6) != None:
        score += shape_score[score_pos6]
    return score

def check_pos(pos):
    if pos[0] < COLUMN and pos[1] <ROW and pos[0]>0 and pos[1]>0:
        return True
    else:
        return False

def game_win(list):
    for m in range(COLUMN + 1):
        for n in range(ROW + 1):

            # 判赢条件 ：横,竖,左斜,右斜 共四个方向，若连子为5则判赢；
            if n < ROW +1 - 4 and (m, n) in list and (m, n + 1) in list and (m, n + 2) in list and (
                    m, n + 3) in list and (m, n + 4) in list:
                return True
            elif m < ROW + 1 - 4 and (m, n) in list and (m + 1, n) in list and (m + 2, n) in list and (
                    m + 3, n) in list and (m + 4, n) in list:
                return True
            elif m < ROW +1 - 4 and n < ROW + 1 - 4 and (m, n) in list and (m + 1, n + 1) in list and (
                    m + 2, n + 2) in list and (m + 3, n + 3) in list and (m + 4, n + 4) in list:
                return True
            elif m < ROW +1 - 4 and n > 3 and (m, n) in list and (m + 1, n - 1) in list and (
                    m + 2, n - 2) in list and (m + 3, n - 3) in list and (m + 4, n - 4) in list:
                return True
    return False


def find_posible(list_human,list_AI, more = 2):
    posi_list = []
    for pos in list_human:
        for num1 in range (0,3):
            for num2 in range(0,3):
                pos0 = pos[0]+num1
                pos1 = pos[1]+num2
                if pos0 < COLUMN and pos1 <ROW and pos0>0 and pos1>0:
                    posi_list.append((pos0,pos1))
                pos0 = pos[0] - num1
                pos1 = pos[1] - num2
                if pos0 < COLUMN and pos1 <ROW and pos0>0 and pos1>0:
                    posi_list.append((pos0,pos1))
                pos0 = pos[0] + num1
                pos1 = pos[1] - num2
                if pos0 < COLUMN and pos1 <ROW and pos0>0 and pos1>0:
                    posi_list.append((pos0,pos1))
                pos0 = pos[0] - num1
                pos1 = pos[1] + num2
                if pos0 < COLUMN and pos1 <ROW and pos0>0 and pos1>0:
                    posi_list.append((pos0,pos1))

    for pos in list_human:
        for num1 in range (0, more):
            for num2 in range(0,more):
                pos0 = pos[0]+num1
                pos1 = pos[1]+num2
                if pos0 < COLUMN and pos1 <ROW and pos0>0 and pos1>0:
                    posi_list.append((pos0,pos1))
                pos0 = pos[0] - num1
                pos1 = pos[1] - num2
                if pos0 < COLUMN and pos1 <ROW and pos0>0 and pos1>0:
                    posi_list.append((pos0,pos1))
                pos0 = pos[0] + num1
                pos1 = pos[1] - num2
                if pos0 < COLUMN and pos1 <ROW and pos0>0 and pos1>0:
                    posi_list.append((pos0,pos1))
                pos0 = pos[0] - num1
                pos1 = pos[1] + num2
                if pos0 < COLUMN and pos1 <ROW and pos0>0 and pos1>0:
                    posi_list.append((pos0,pos1))
    p_list = sorted(set(posi_list), key=posi_list.index)
    for pos in list_human:
        for i in range(0, len(p_list)):
            if(p_list[i] == pos):
                p_list.pop(i)
                break
    for pos in list_AI:
        for i in range(0, len(p_list)):
            if(p_list[i] == pos):
                p_list.pop(i)
                break
    return p_list

