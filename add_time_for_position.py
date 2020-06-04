# -*- coding: utf-8 -*-
'''为猫物实体的“官职”陈述添加“始于时间线”限定符。'''
import pywikibot
from pywikibot import pagegenerators
from utils import zh2cp

def get_pos_field(pos, text):
    pos_codes = {
        'medicine cat': 'medicine_cat',
        'clan leader': 'leader',
        'Softpaw': 'softpaw',
        'Sharpclaw': 'sharpclaw',
        'To-Be': 'to_be',
        'Cave-Guard': 'cave_guard',
        'Prey-Hunter': 'prey_hunter',
        'Kit-Mother': 'kit_mother',
        'guardian cats': 'guardian_cat',
        'daylight warrior': 'warrior'
        }
    if '|guardian_healer_name=' in text:
        pos_codes['healer'] = 'guardian_healer'
    if pos in pos_codes:
        return pos_codes[pos] + '_name'
    else:
        return pos + '_name'

def get_next_field(field, text):
    fields = ['kittypet_name', 'loner_name', 'rogoue_name', 'kit_name',
        'apprentice_name', 'warrior_name', 'medicine_cat_name', 'queen_name',
        'deputy_name', 'leader_name', 'elder_name', 'father']
    fields_guard = ['kittypet_name', 'loner_name', 'rogue_name',
        'guardian_healer_name', 'guardian_cat_name', 'kit_name',
        'apprentice_name', 'warrior_name', 'medicine_cat_name', 'queen_name',
        'deputy_name', 'leader_name', 'elder_name', 'known_name', 'father']
    fields_alt = ['softpaw_name', 'kittypet_name', 'ancient_name', 'loner_name',
        'rogue_name', 'kit_name', 'early_settler_name', 'apprentice_name',
        'to_be_name', 'warrior_name', 'sharpclaw_name', 'cave_guard_name', 'prey_hunter_name',
        'medicine_cat_name', 'healer_name', 'queen_name', 'kit_mother_name',
        'deputy_name', 'leader_name', 'elder_name', 'father']
    if '|ancient_name' in text:
        count = 1
        while fields_alt[fields_alt.index(field) + count] not in text:
            count += 1
        return fields_alt[fields_alt.index(field) + count]
    if '|guardian' in text:
        count = 1
        while fields_guard[fields_guard.index(field) + count] not in text:
            count += 1
        return fields_guard[fields_guard.index(field) + 1]
    else:
        count = 1
        while fields[fields.index(field) + count] not in text:
            count += 1
        return fields[fields.index(field) + 1]

if __name__ == '__main__':
    site_zh = pywikibot.Site('zh', 'zhwarriorswiki')
    site_cp = pywikibot.Site('en', 'crystalpool')
    repo = site_cp.data_repository()

    # continue from last interruption
    start = False
    for title in zh2cp.characters:
        if title == '莉薇':
            start = True
        if start:
            print(title)
            page = pywikibot.Page(site_zh, title)
            item = pywikibot.ItemPage(repo, zh2cp.characters[title])
            item.get()
            if 'P83' not in item.claims: continue # 官职
            for clm in item.claims['P83']:
                if 'P92' in clm.qualifiers: continue
                tar = clm.getTarget()
                if type(tar) != pywikibot.ItemPage: continue
                tar.get()
                field = get_pos_field(tar.labels['en'], page.text)
                pos_start = page.text.index('|{0}'.format(field))
                pos_end = page.text.index('|{0}'.format(get_next_field(field,
                    page.text)))
                cite_start_content = '{{r|'
                cite_start = page.text.find(cite_start_content, pos_start,
                    pos_end) + len(cite_start_content)
                if cite_start == len(cite_start_content) - 1: continue
                cite_end = page.text.index('}}', cite_start)
                cite = page.text[cite_start:cite_end]
                if '|' in cite: cite = cite[:cite.index('|')]
                if cite in zh2cp.works:
                    print(cite)
                    work = pywikibot.ItemPage(repo, zh2cp.works[cite])
                    qualifier = pywikibot.Claim(repo, 'P92') # 始于时间线
                    qualifier.setTarget(work)
                    clm.addQualifier(qualifier)
