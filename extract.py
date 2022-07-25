from cocoNLP.extractor import extractor
import pkuseg
import re

path = 'docs_utf8'
# ner = []
ex = extractor()
# nlp_ch = StanfordCoreNLP('stanford-corenlp-4.2.2', lang='zh')
seg = pkuseg.pkuseg(postag=True)  # 加载模型，给定用户词典


def info_extract(txt_list):
    result_list = []

    for txt in txt_list:
        print('running extract... ' + str(txt))
        d = {}
        f = open(path + '\\' + str(txt) + '.txt', 'r',encoding='utf-8')
        raw_text = f.read().replace('\n', '').replace('\\', '')
        f.close()
        text = raw_text.split('【 正  文 】')[1]
        # global ner
        # ner = nlp_ch.ner(text)
        # print(ner)
        find_art(raw_text, d)
        find_name(text, d)
        find_location(text, d)
        find_time(text, d)
        find_book(text, d)
        result_list.append(d)
    # nlp_ch.close()
    return to_string(result_list)[0]


def to_string(input_list: list):
    result_list = []
    for d in input_list:
        string = ''
        for key in d.keys():
            string = string + '【' + key + '】'
            for element in d[key]:
                string = string + element + ' | '
            string = string[:-len(' | ')]
            string = string + '\n'
        result_list.append(string)
        # print(string, end='')
    return result_list


def find_art(string: str, d: dict):
    to_find_list = {'美术', '音乐', '舞蹈', '文学', '戏剧', '影视', '摄影', '曲艺', '杂技', '建筑', '园林',
                    '电影', '电视', '绘画', '雕塑', '书法', '戏曲', '诗歌', '散文', '小说', '陶艺'}
    pos_list = seg.cut(string)
    arts = []
    for w in pos_list:
        if w[0] in to_find_list:
            arts.append(w[0])
    arts = list(set(arts))
    if len(arts) == 0:
        arts.append('无')
    d['艺术类别'] = arts


def find_name(string: str, d: dict):
    names = ex.extract_name(string)
    names = list(set(names))
    if len(names) == 0:
        names.append('无')
    d['人物'] = names


def find_location(string: str, d: dict):
    locations = ex.extract_locations(string)
    locations = list(set(locations))
    if len(locations) == 0:
        locations.append('无')
    d['地点'] = locations


def find_time(string: str, d: dict):
    times = []
    # for t in ner:
    #     if t[1] == 'DATE':
    #         times.append(t[0])
    pos_list = seg.cut(string)
    for w in pos_list:
        if w[1] == 't':
            times.append(w[0])
    times = list(set(times))
    if len(times) == 0:
        times.append('无')
    d['时间'] = times


def find_book(string: str, d: dict):
    pattern = re.compile(r'《(.*?)》')
    books = pattern.findall(string)
    books = list(set(books))
    for i in range(len(books)):
        books[i] = '《' + books[i] + '》'
    if len(books) == 0:
        books.append('无')
    d['作品'] = books


if __name__ == '__main__':
    txt_list = [20, 88]
    result = info_extract(txt_list)
    print(*result)
