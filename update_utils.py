# -*- coding: utf-8 -*-
'''Update utils/ with query results from Crystal Pool.'''
import ssl
import urllib.request
import rdflib

graph = rdflib.Graph()
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
with urllib.request.urlopen(
    'https://raw.githubusercontent.com/crystal-pool/Dump/master/wbdump.ttl',
    context=ctx) as dump:
    graph.parse(format='n3', data=dump.read().decode('utf-8'))

zh2cp_characters_query = graph.query('''
SELECT ?page ?character
{
    ?character wdt:P3/wdt:P4* wd:Q624 .
    ?sitelink schema:inLanguage "zh" ;
              schema:about ?character ;
              schema:name ?page .
}''')
zh2cp_characters_results = {}
for row in zh2cp_characters_query:
    zh2cp_characters_results[row.page.value] = row.character.rpartition('/')[-1]

zh2cp_books_query = graph.query('''
SELECT ?page ?book
{
    ?book wdt:P3 wd:Q46 .
    ?sitelink schema:inLanguage "zh" ;
              schema:about ?book ;
              schema:name ?page .
}''')
zh2cp_books_results = {}
for row in zh2cp_books_query:
    zh2cp_books_results[row.page.value] = row.book.rpartition('/')[-1]

zh2cp_works_query = graph.query('''
SELECT ?code ?work
{
    ?work wdt:P50?/wdt:P3 wd:Q46 ;
          skos:altLabel ?code .
    FILTER (lang(?code) = "en")
}''')
zh2cp_works_results = {}
for row in zh2cp_works_query:
    if '-' in row.code.value:
        zh2cp_works_results[row.code.value.lower().replace('-', '[') + ']'] = (
            row.work.rpartition('/')[-1])
    else:
        zh2cp_works_results[row.code.value.lower()] = (row.work
            .rpartition('/')[-1])

zh2cp = {
    'characters': zh2cp_characters_results,
    'books': zh2cp_books_results,
    'works': zh2cp_works_results
    }
with open('utils/zh2cp.py', 'w') as f:
    f.write('# -*- coding: utf-8 -*-\n\n')
with open('utils/zh2cp.py', 'a') as f:
    for key in zh2cp:
        f.write('{0} = {1}\n'.format(key, zh2cp[key]))

cp2zh = {
    'characters': {},
    'books': {},
    'works': {}
    }

for character in zh2cp_characters_results:
    cp2zh['characters'][zh2cp_characters_results[character]] = character
for book in zh2cp_books_results:
    cp2zh['books'][zh2cp_books_results[book]] = book
for work in zh2cp_works_results:
    cp2zh['works'][zh2cp_works_results[work]] = work

with open('utils/cp2zh.py', 'w') as f:
    f.write('# -*- coding: utf-8 -*-\n\n')
with open('utils/cp2zh.py', 'a') as f:
    for key in cp2zh:
        f.write('{0} = {1}\n'.format(key, cp2zh[key]))
