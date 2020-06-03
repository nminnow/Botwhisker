# -*- coding: utf-8 -*-
'''Logs executed scripts with execution date in UTC+0.'''
from datetime import datetime
import sys

if __name__ == '__main__':
    with open('log.txt', 'a') as f:
        now = datetime.utcnow()
        for argv in sys.argv[1:]:
            script = __import__(argv)
            f.write('{0}-{1}-{2} {3} {4}\n'.format(now.year, now.month, now.day,
                argv, script.__doc__))