# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, unicode_literals

from pywikibot import family
from pywikibot.tools import deprecated


class Family(family.Family):  # noqa: D101

    name = 'zhwarriorswiki'
    langs = {
        'zh': 'warriors.huijiwiki.com',
    }

    def scriptpath(self, code):
        return {
            'zh': '',
        }[code]

    @deprecated('APISite.version()', since='20141225')
    def version(self, code):
        return {
            'zh': '1.30.0',
        }[code]

    def protocol(self, code):
        return {
            'zh': 'https',
        }[code]
