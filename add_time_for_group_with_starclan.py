# -*- coding: utf-8 -*-
'''为拥有两个“所属组织”陈述且其中包含“星族”的实体添加“始于时间线/终于时间线：未知值”修饰。'''
import pywikibot

site = pywikibot.Site('en', 'crystalpool')
repo = site.data_repository()

items = ['Q725', 'Q729', 'Q731', 'Q732', 'Q733', 'Q2311', 'Q2317', 'Q2333', 'Q2372', 'Q2377', 'Q2399', 'Q2414', 'Q2419', 'Q2420', 'Q2434', 'Q2446', 'Q2457', 'Q2474', 'Q2489', 'Q2491', 'Q2496', 'Q2506', 'Q2525', 'Q2549', 'Q2619', 'Q2601', 'Q2658', 'Q2665', 'Q2709', 'Q2728', 'Q2761', 'Q2808', 'Q2882', 'Q2916', 'Q2963', 'Q2968', 'Q2992', 'Q3022', 'Q3062', 'Q3033', 'Q3085', 'Q3095', 'Q3164', 'Q3178', 'Q3189', 'Q3313', 'Q3334', 'Q3353', 'Q3361', 'Q3403', 'Q3461', 'Q3430', 'Q3476', 'Q3482', 'Q3600', 'Q3601', 'Q3602', 'Q3517', 'Q3603', 'Q3613', 'Q3615', 'Q3616', 'Q3538', 'Q3617', 'Q3618', 'Q3620', 'Q3550', 'Q3643', 'Q3596', 'Q3718', 'Q3597', 'Q3719', 'Q3598', 'Q4104', 'Q3599', 'Q4105', 'Q4106']
# SELECT DISTINCT ?cat
# {
#     ?cat p:P76 ?group .
#     ?group ps:P76 wd:Q634 .
#     FILTER NOT EXISTS { ?group pq:P92 ?startTime }
# }
start_point = pywikibot.Claim(repo, 'P92') # 始于时间线
end_point = pywikibot.Claim(repo, 'P93') # 终于时间线

for itm in items:
    item = pywikibot.ItemPage(repo, itm)
    item.get()
    if len(item.claims['P76']) == 2: # 所属组织
        for clm in item.claims['P76']:
            if clm.getTarget() == pywikibot.ItemPage(repo, 'Q634'): # 星族
                if 'P92' not in clm.qualifiers:
                    start_point.on_item = None
                    start_point.setSnakType('somevalue')
                    clm.addQualifier(start_point)
            else:
                if 'P93' not in clm.qualifiers:
                    end_point.on_item = None
                    end_point.setSnakType('somevalue')
                    clm.addQualifier(end_point)
