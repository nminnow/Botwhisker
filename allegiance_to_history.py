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
    if the_book_title not in text:
        history_start = (text.index(HISTORY_START_CONTENT) +
                         len(HISTORY_START_CONTENT))
        history_end = text.index(HISTORY_END_CONTENT, history_start)
        the_set_start = text.index(the_set_title, history_start, history_end)
        if the_set_start == -1:
            sets = re.findall('\n=== (.*) ===', text[history_start:history_end])
            set_after = ''
            for set in sets:
                set_rank = all_sets.index(set)
                if set_rank > the_set_rank:
                    set_after = set
                    break
            if len(set_after) == 0:
                text_before = text[:history_end]
                text_after = text[history_end:]
            else:
                set_after_start = text.index('\n=== {} ==='.format(set_after))
                text_before = text[:set_after_start]
                text_after = text[set_after_start:]
            text = text_before + the_set_title + the_book_title + the_book_text
                + text_after
        else:
            the_set_start += len(the_set_title)
            the_set_end = text.find(SET_END_CONTENT, the_set_start, history_end)
            if the_set_end == -1:
                the_set_end = history_end
            books = findall('\n==== 《\[\[(.*)\]\]》 ====',
                text[the_set_start:the_set_end])
            book_after = ''
            for book in books:
                book_rank = all_books.index(book)
                if book_rank > the_book_rank:
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
            text = text_before + the_book_title + the_book_text + text_after
    return text

HISTORY_START_CONTENT = '\n== 生平 =='
HISTORY_END_CONTENT = '\n== '
SET_END_CONTENT = '\n=== '

with open('utils/all_books.txt', 'r') as fr:
    all_books = [line.strip() for line in fr.readlines()]
with open('utils/all_sets.txt', 'r') as fr:
    all_sets = [line.strip() for line in fr.readlines()]

the_book = input('书籍名称（例如：蛾翅的秘密）：')
if the_book not in all_books:
    print('书籍{0}未被收录。以下是所有已收录书籍和它们的编号。'.format(the_book))
    for book in all_books:
        print('{0}: {1}'.format(all_books.index(book), book))
    the_book_rank = input('请输入该书籍应有的编号：')
    all_books = all_books[:the_book_rank] + the_book + all_books[the_book_rank:]
    with open('utils/all_books.txt', 'w') as fw:
        for book in all_books:
            fw.write('{0}\n'.format(book))
    print('收录完毕。')
else:
    the_book_rank = all_books.index(the_book)

the_set = input('书籍属于系列（例如：[[短篇电子书]]）：')
if the_set not in all_sets:
    print('系列{0}未被收录。以下是所有已收录系列和它们的编号。'.format(the_set))
    for set in all_sets:
        print('{0}: {1}'.format(all_sets.index(set), set))
    the_set_rank = input('请输入该系列应有的编号：')
    all_sets = all_sets[:the_set_rank] + the_set + all_sets[the_set_rank:]
    with open('utils/all_sets.txt', 'w') as fw:
        for set in all_sets:
            fw.write('{0}\n'.format(set))
    print('收录完毕。')
else:
    the_set_rank = all_sets.index(the_set)

the_book_title = '\n==== 《[[{}]]》 ===='.format(the_book)
the_set_title = '\n=== {} ==='.format(the_set)
the_book_text = '\n{{{{Coming soon}}}}\n\n{{{{章节分隔线}}}}\n'.format(the_book)

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
        page.save('/*生平*/添加章节：《[[{0}]]》'.format(the_book))
