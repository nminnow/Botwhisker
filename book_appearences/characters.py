# -*- coding: utf-8 -*-
'''按照猫武士中文维基对应猫物表页面为图书实体添加“登场角色”陈述。'''
import pywikibot
from pywikibot import pagegenerators
from utils import zh2cp

site_zh = pywikibot.Site('zh', 'zhwarriorswiki')
site_cp = pywikibot.Site('en', 'crystalpool')
repo = site_cp.data_repository()
claim = pywikibot.Claim(repo, 'P119')
book = input('请输入书籍名称（例如“日落和平”）：')
item = pywikibot.ItemPage(repo, input('请输入书籍实体编号（例如“Q144”）：'))

chars = []
for page in pagegenerators.LinkedPageGenerator(pywikibot.Page(site_zh,
    '{}/猫物表'.format(book))):
    if pywikibot.Category(site_zh, 'Category:猫物') in list(page.categories()):
        chars.append(zh2cp.cats[page.title()])

for char in chars:
    claim.setTarget(pywikibot.ItemPage(repo, char))
    item.addClaim(claim)