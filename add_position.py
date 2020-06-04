# -*- coding: utf-8 -*-
'''为猫物实体添加“官职”陈述。'''
import re
import pywikibot
from utils import zh2cp

if __name__ == '__main__':
    site_zh = pywikibot.Site('zh', 'zhwarriorswiki')
    site_cp = pywikibot.Site('en', 'crystalpool')
    repo = site_cp.data_repository()

    ALL_POSITIONS = {
        'healer': 'Q672', # 尖石的预言者
        'apprentice': 'Q681', # 学徒
        'warrior': 'Q682', # 武士
        'medicine_cat': 'Q684', # 巫医
        'queen': 'Q685', # 猫后
        'deputy': 'Q686', # 副族长
        'leader': 'Q688', # 族长
        'elder': 'Q692', # 长老
        'leader_NotClan': 'Q694', # 首领
        'to_be': 'Q696', # 半大猫
        'cave_guard': 'Q697', # 护穴猫
        'prey_hunter': 'Q698', # 狩猎猫
        'kit_mother': 'Q699', # 猫妈妈
        'softpaw': 'Q700', # 柔掌
        'sharpclaw': 'Q701', # 利爪
        'hunter': 'Q702', # 猎者
        'guardian_healer': 'Q705', # 治疗者
        'guardian_cat': 'Q710' # 守护者
        }

    for title in zh2cp.characters:
        print(title)
        item = pywikibot.ItemPage(repo, zh2cp.characters[title])
        item.get()

        tars = []
        if 'P83' in item.claims: # 官职
            for clm in item.claims['P83']:
                tars.append(clm.getTarget())

        page = pywikibot.Page(site_zh, title)
        fields = re.findall('\\|(.*)_name *= .', page.text)

        positions = []
        for field in fields:
            if field in ALL_POSITIONS:
                positions.append(ALL_POSITIONS[field])

        for pos in positions:
            position = pywikibot.ItemPage(repo, pos)
            if position not in tars:
                print(pos)
                claim = pywikibot.Claim(repo, 'P83')
                claim.setTarget(position)
                item.addClaim(claim)
