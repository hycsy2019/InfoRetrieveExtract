# 对查询结果进行输出
path_doc = 'docs_utf8'  # 原始文档存储目录


def OutputDoc(Sim, rankL, rankH):
    '''输出排名rankL到rankH之间的文档结果'''
    L = []  # 存储所有查询结果的列表
    file_list = []

    count = 1
    for each in Sim:
        if count < rankL:  # 未到达排名左区间
            count += 1
            continue

        if count > rankH:  # 超出排名右区间
            break

        if each[1][0][0] == 0:
            break  # 如果相关度为0则退出

        file_list.append(each[0])

        entry = '【 相关度 】' + str(each[1][0][0])+'\n'  # 将相关度加入输出
        f = open(path_doc + '\\' + str(each[0]) + '.txt', 'rb')
        s = f.read().decode('utf-8').split('【 正  文 】')[0]
        entry += s.replace('\n','').replace('\r','').replace('【','\n【')[1:]+'\n'

        f.close()

        count += 1
        L.append(entry)

    return L, file_list


def OutputThings(listtest, txtnum):
    '''输出主要匹配内容'''
    L = []
    for each in txtnum:
        res = ''
        fp = open('docs_utf8\\' + str(each) + '.txt', 'r', encoding='utf-8')
        text = fp.read().split('【 正  文 】')[1]

        for word in listtest:
            text = text.replace(word, '『' + word + '』')  # 将关键词加上括号

        for word in listtest:
            pos = text.find(word)
            if pos == -1:
                continue
            if pos - 50 > 0:  # 输出关键词附近的内容
                res = res + '...' + text[(pos - 50):(pos + 100)] + '...'
            else:
                res = res + '...' + text[0:(pos + 50)] + '...'

        L.append(res.replace('\n', ''))

    return L

# Result=OutputDoc(1,10)
