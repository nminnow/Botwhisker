from timeline.books import *

years = {}

for book in books:
    for chapter in books[book]:
        year = books[book][chapter][0]
        month = books[book][chapter][1]
        if year not in years:
            years[year] = {}
        if month not in years[year]:
            years[year][month] = []
        years[year][month].append([book, chapter])

with open('timeline/years.py', 'w') as f:
    f.write('years = {0}'.format(repr(years)))
