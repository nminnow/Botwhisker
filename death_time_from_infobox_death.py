# -*- coding: utf-8 -*-
'''从猫武士中文维基猫物页面信息栏中死因一栏获取死亡时间并导入至水晶池中相应实体。'''
import re
import pywikibot
from pywikibot import pagegenerators
from utils import zh2cp

site_zh = pywikibot.Site('zh', 'zhwarriorswiki')
site_cp = pywikibot.Site('en', 'crystalpool')
repo = site_cp.data_repository()
claim = pywikibot.Claim(repo, 'P96') # death time on timeline

for page in pagegenerators.CategorizedPageGenerator(pywikibot.Category(site_zh,
    'Category:猫物')):
    print(page.title())
    item = pywikibot.ItemPage(repo, zh2cp.cats[page.title()])
    item.get()
    if 'P96' in item.claims: continue
    death_refs =  re.findall('\{\{COD.*\}\}\{\{r\|(.*)\}\}', page.text)
    if len(death_refs) == 0: continue
    death_time = death_refs[0]
    if '|' in death_time: death_time = death_time[:death_time.index('|')]
    if death_time not in zh2cp.works: continue
    claim.setTarget(pywikibot.ItemPage(repo, zh2cp.works[death_time]))
    item.addClaim(claim)
