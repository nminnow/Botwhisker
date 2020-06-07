# -*- coding: utf-8 -*-
'''为猫物实体的“官职”陈述添加“始于时间线”限定符。'''
import pywikibot
from utils import zh2cp

if __name__ == '__main__':
    site_zh = pywikibot.Site('zh', 'zhwarriorswiki')
    site_cp = pywikibot.Site('en', 'crystalpool')
    repo = site_cp.data_repository()

    ALL_POSITIONS = {
        'Q672': 'healer', # 尖石的预言者
        'Q681': 'apprentice', # 学徒
        'Q682': 'warrior', # 武士
        'Q684': 'medicine_cat', # 巫医
        'Q685': 'queen', # 猫后
        'Q686': 'deputy', # 副族长
        'Q688': 'leader', # 族长
        'Q692': 'elder', # 长老
        'Q694': 'leader_NotClan', # 首领
        'Q696': 'to_be', # 半大猫
        'Q697': 'cave_guard', # 护穴猫
        'Q698': 'prey_hunter', # 狩猎猫
        'Q699': 'kit_mother', # 猫妈妈
        'Q700': 'softpaw', # 柔掌
        'Q701': 'sharpclaw', # 利爪
        'Q702': 'hunter', # 猎者
        'Q705': 'guardian_healer', # 治疗者
        'Q710': 'guardian_cat' # 守护者
        }

    for title in zh2cp.characters:
        print(title)
        page = pywikibot.Page(site_zh, title)
        item = pywikibot.ItemPage(repo, zh2cp.characters[title])
        item.get()
        if 'P83' not in item.claims: continue # 官职
        for clm in item.claims['P83']:
            if type(clm.getTarget()) != pywikibot.ItemPage: continue
            position = clm.getTarget().title()[5:] # strip out Item: prefix
            if position not in ALL_POSITIONS: continue
            field_start = page.text.index('|{0}_name'.format(ALL_POSITIONS
                [position]))
            field_end = field_start + page.text[field_start:].index('\n')
            code_start = field_start + page.text[field_start:field_end].find(
                '{{r|') + 4
            if code_start == field_start + 3: continue
            code_end = code_start + page.text[code_start:field_end].index('}}')
            code = page.text[code_start:code_end]
            if '|' in code:
                code = code[:code.index('|')]
            if code not in zh2cp.works: continue
            work = pywikibot.ItemPage(repo, zh2cp.works[code])
            qualifier = pywikibot.Claim(repo, 'P92') # 始于时间线
            qualifier.setTarget(work)
            clm.addQualifier(qualifier)
