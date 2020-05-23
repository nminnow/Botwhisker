# -*- coding: utf-8 -*-
'''
新书出版后为猫物页面中的生平部分添加相应章节。

效果：
https://warriors.huijiwiki.com/index.php?title=%E8%9B%BE%E7%BF%85&diff=prev&oldid=112476
https://warriors.huijiwiki.com/index.php?title=%E9%BC%A9%E9%BC%B1%E7%88%AA&diff=prev&oldid=112498
'''
from re import findall
import pywikibot
from pywikibot import pagegenerators

def add_history(text):
    if not the_book_title in text:
        history_start = (text.index(HISTORY_START_CONTENT) +
                         len(HISTORY_START_CONTENT))
        history_end = text.index(HISTORY_END_CONTENT, history_start)
        if text.find(the_set_title, history_start, history_end) == -1:
            sets = re.findall('\n=== (.*) ===', text[history_start:history_end])
            set_before = ''
            set_after = ''
            for set in sets:
                set_rank = ALL_SETS.index(set)
                if set_rank < the_set_rank:
                    set_before = set
                elif set_rank > the_set_rank:
                    set_after = set
                    break
            if len(set_after) == 0:
                text_before = text[:history_end]
                text_after = text[history_end:]
            else:
                set_after_start = text.index('\n=== {} ==='.format(set_after))
                text_before = text[:set_after_start]
                text_after = text[set_after_start:]
            text = text_before + the_set_title + the_book_text + text_after
        else:
            the_set_start = text.index(the_set_title, history_start,
                                       history_end) + len(the_set_title)
            the_set_end = (text.index(SET_END_CONTENT, the_set_start,
                                      history_end)
                if text.find(SET_END_CONTENT, the_set_start, history_end) != -1
                else history_end)
            books = findall('\n==== 《\[\[(.*)\]\]》 ====',
                            text[the_set_start:the_set_end])
            book_before = ''
            book_after = ''
            for book in books:
                book_rank = ALL_BOOKS.index(book)
                if book_rank < the_book_rank:
                    book_before = book
                elif book_rank > the_book_rank:
                    book_after = book
                    break
            if len(book_after) == 0:
                text_before = text[:the_set_end]
                text_after = text[the_set_end:]
            else:
                book_after_start = text.index('\n==== 《[[{}]]》 ===='
                                              .format(book_after))
                text_before = text[:book_after_start]
                text_after = text[book_after_start:]
            text = text_before + the_book_text + text_after
    return text

ALL_BOOKS = ['族群的秘密', '族群的猫', '族群的守则', '族群的战争', '进入族群', '终极指南', '武士指南', '追随太阳', '雷电崛起', '首次战争', '燃烧之星', '占地为王', '群星之路', '蛾飞的幻象', '雷星的怀响', '影星的生命', '云星的旅程', '枫荫的复仇', '松星的抉择', '鹅羽的诅咒', '高星的复仇', '钩星的承诺', '蓝星的预言', '黄牙的秘密', '长鞭崛起', '斑叶的心声', '红尾的恩债', '呼唤野性', '寒冰烈火', '疑云重重', '虎掌的愤怒', '风起云涌', '险路惊魂', '进入森林', '逃出森林', '力挽狂澜', '返回族群', '火星的探索', '和平破碎', '族群救星', '武士之心', '天族外传', '蛾翅的秘密', '午夜追踪', '新月危机', '重现家园', '武士失踪', '武士避难', '叶池的希望', '武士回归', '紧急救援', '星光指路', '超越规则', '黄昏战争', '洪水过后', '日落和平', '灰条历险记', '预视力量', '暗河汹涌', '驱逐之战', '天蚀遮月', '暗夜长影', '拂晓之光', '冬青叶的故事', '第四学徒', '战声渐近', '雾星的征兆', '乌爪的告别', '暗夜密语', '月光印记', '武士归来', '群星之战', '鹰翅的旅程', '卵石光的幼崽', '鸽翅的沉默', '鸦羽的拷问', '阿树的根源', '黑莓星的风暴', '学徒探索', '雷影交加', '天空破碎', '极夜无光', '虎心的阴影', '烈焰焚河', '褐皮的族群', '风暴来袭', '松鼠飞的希望', '迷失群星', 'The Silent Thaw', 'Veil of Shadows', 'Darkness Within']
ALL_SETS = ['[[长篇外传]]', '[[族群黎明]]', '[[预言开始]]', '[[新预言]]', '[[三力量]]', '[[星预言]]', '[[暗影幻象]]', '[[破灭守则]]', '[[短篇电子书]]', '[[乌爪的旅程]]', '[[灰条历险记]]', '[[天族与陌生者]]', '[[荒野手册]]', '[[短篇故事]]', '其他']
HISTORY_START_CONTENT = '\n== 生平 =='
HISTORY_END_CONTENT = '\n== '
SET_END_CONTENT = '\n=== '

the_book = input('书籍名称（例如：蛾翅的秘密）：')
the_set = input('书籍属于系列（例如：[[短篇电子书]]）：')
the_book_rank = ALL_BOOKS.index(the_book)
the_set_rank = ALL_SETS.index(the_set)
the_book_title = '\n==== 《[[{}]]》 ===='.format(the_book)
the_set_title = '\n=== {} ==='.format(the_set)
the_book_text = (the_book_title + '\n{{{{Coming soon}}}}\n\n{{{{章节分隔线}}}}\n'
                                  .format(the_book))

site = pywikibot.Site('zh', 'zhwarriorswiki')
for page in (pagegenerators.LinkedPageGenerator(pywikibot.Page(site, '{}/猫物表'
    .format(the_book)))):
    if pywikibot.Category(site, 'Category:猫物') in list(page.categories()):
        if page.isRedirectPage():
            page = page.getRedirectTarget()
        history_page = pywikibot.Page(site, '{}/生平'.format(title))
        if history_page.exists():
            page = history_page
        page.text = add_history(page.text)
        page.save()
