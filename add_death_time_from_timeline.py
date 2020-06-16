# -*- coding: utf-8 -*-
'''为猫物实体添加获取自“时间轴”条目的“死亡于时间线”陈述。'''
import re
import pywikibot
from utils import cp2zh
from utils import zh2cp
from utils.timeline.years import years

if __name__ == '__main__':
    zh = pywikibot.Site('zh', 'zhwarriorswiki')
    cp = pywikibot.Site('en', 'crystalpool')
    repo = cp.data_repository()
    timeline = pywikibot.Page(zh, '时间轴').text

    N = 1000
    M = 2000
    SEASONS = {
        '新叶季': 3,
        '绿叶季': 6,
        '落叶季': 9,
        '秃叶季': 12
        }

    xs = re.findall('=== ([N\\+0-9]*)年 ===\n\\{\\{时间轴\n(.*)\\}\\}\n\n==',
        timeline, flags=re.DOTALL)
    for x in xs:
        year = M + x[0] if 'N' not in x[0] else N + int(x[0][2:])
        ys = re.findall('\\|(.*)死亡=(.*)', x[1])
        for y in ys:
            season = SEASONS[y[0]]
            zs = re.findall('\\[\\[([^\\|\\]]*)[\\|\\]]', y[1])
            print(zs)
            for z in zs:
                item = pywikibot.ItemPage(repo, zh2cp.characters[z])
                item.get()

                if 'P96' in item.claims: continue # 死亡于时间线
                byear = year
                bseason = season
                while True:
                    try:
                        book = cp2zh.works[years[byear][bseason][0][0]]
                    except KeyError:
                        if bseason == 12:
                            bseason = 3
                            byear += 1
                        else:
                            bseason += 3
                        continue
                    else:
                        chapter = years[byear][bseason][0][1]
                        break
                claim = pywikibot.Claim(repo, 'P96')
                ctarget = pywikibot.ItemPage(repo, zh2cp.works[
                    '{0}[{1}]'.format(book, chapter)])
                claim.setTarget(ctarget)
                print(zh2cp.works['{0}[{1}]'.format(book, chapter)])
                item.addClaim(claim)

                if byear == year and bseason == season: continue
                item.get()
                qualifier = pywikibot.Claim(repo, 'P94') # 时间线位移
                moon = - (12 * (byear - year) + (bseason - season))
                qtarget = pywikibot.WbQuantity(moon, unit=pywikibot.ItemPage(
                    repo, 'Q2294'), site=cp) # 月
                qualifier.setTarget(qtarget)
                print(moon)
                item.claims['P96'][0].addQualifier(qualifier)
