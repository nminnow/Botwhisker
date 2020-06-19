# -*- coding: utf-8 -*-
'''Update utils/ with query results from Crystal Pool.'''
import ssl
import sys
import urllib.request
import rdflib

def init_graph():
    print('Initializing graph...')
    global graph
    graph = rdflib.Graph()
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    with urllib.request.urlopen('https://raw.githubusercontent.com/crystal-pool/Dump/master/wbdump.ttl',
        context=ctx) as dump:
        graph.parse(format='n3', data=dump.read().decode('utf-8'))
    print('Finished initializing graph.')

def en2cp():
    print('Executing en2cp...')
    if 'graph' not in globals():
        init_graph()

    en2cp_characters_query = graph.query('''
SELECT ?page ?character
{
    ?character wdt:P3/wdt:P4*    wd:Q624 .
    ?sitelink  schema:inLanguage "en" ;
               schema:about      ?character ;
               schema:name       ?page .
}
''')
    en2cp_characters = {}
    for row in en2cp_characters_query:
        en2cp_characters[row[0].value] = row[1].rpartition('/')[-1]

    en2cp_books_query = graph.query('''
SELECT ?page ?book
{
    ?book     wdt:P3            wd:Q46 .
    ?sitelink schema:inLanguage "en" ;
              schema:about      ?book ;
              schema:name       ?page .
}
''')
    en2cp_books = {}
    for row in en2cp_books_query:
        en2cp_books[row[0].value] = row[1].rpartition('/')[-1]

    en2cp = {
        'characters': en2cp_characters,
        'books': en2cp_books
    }
    with open('utils/en2cp.py', 'w') as f:
        f.write('# -*- coding: utf-8 -*-\n\n')
        for k in en2cp:
            f.write('{0} = {1}\n'.format(k, en2cp[k]))
    print('Finished executing en2cp.')

def zh2cp():
    print('Executing zh2cp...')
    if graph not in globals():
        init_graph()

    zh2cp_characters_query = graph.query('''
SELECT ?page ?character
{
    ?character wdt:P3/wdt:P4*    wd:Q624 .
    ?sitelink  schema:inLanguage "zh" ;
               schema:about      ?character ;
               schema:name       ?page .
}
''')
    zh2cp_characters = {}
    for row in zh2cp_characters_query:
        zh2cp_characters[row.page.value] = row.character.rpartition('/')[-1]

    zh2cp_books_query = graph.query('''
SELECT ?page ?book
{
    ?book     wdt:P3            wd:Q46 .
    ?sitelink schema:inLanguage "zh" ;
              schema:about      ?book ;
              schema:name       ?page .
}
''')
    zh2cp_books = {}
    for row in zh2cp_books_query:
        zh2cp_books[row.page.value] = row.book.rpartition('/')[-1]

    zh2cp_works_query = graph.query('''
SELECT ?code ?work
{
    ?work wdt:P50?/wdt:P3 wd:Q46 ;
          skos:altLabel   ?code .
    FILTER (lang(?code) = "en")
}
''')
    zh2cp_works = {}
    for row in zh2cp_works_query:
        if '-' in row.code.value:
            zh2cp_works[row.code.value.lower().replace('-', '[') + ']'] = (row.work.rpartition('/')[-1])
        else:
            zh2cp_works[row.code.value.lower()] = (row.work.rpartition('/')[-1])

    zh2cp = {
        'characters': zh2cp_characters,
        'books': zh2cp_books,
        'works': zh2cp_works
        }
    with open('utils/zh2cp.py', 'w') as f:
        f.write('# -*- coding: utf-8 -*-\n\n')
        for k in zh2cp:
            f.write('{0} = {1}\n'.format(k, zh2cp[k]))
    print('Finished executing zh2cp.')

def cp2zh():
    print('Executing cp2zh...')
    try:
        from utils import zh2cp
    except ImportError:
        print('Failed to import zh2cp.')
        zh2cp()

    cp2zh = {
        'characters': {},
        'books': {},
        'works': {}
        }

    for zh, cp in zh2cp.characters.items():
        cp2zh['characters'][cp] = zh

    for zh, cp in zh2cp.books.items():
        cp2zh['books'][cp] = zh

    for zh, cp in zh2cp.works.items():
        if cp in cp2zh['works']:
            cp2zh['works'][cp].append(zh)
        else:
            cp2zh['works'][cp] = [zh]

    with open('utils/cp2zh.py', 'w') as f:
        f.write('# -*- coding: utf-8 -*-\n\n')
        for k in cp2zh.items():
            f.write('{0} = {1}\n'.format(k, cp2zh[k]))
    print('Finished executing cp2zh.')

if __name__ == '__main__':
    for argv in sys.argv[1:]:
        exec('{0}()'.format(argv))
