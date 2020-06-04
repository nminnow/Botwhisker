# -*- coding: utf-8 -*-
'''Logs executed scripts with execution date in UTC+0.'''
from datetime import datetime
import sys

if __name__ == '__main__':
    with open('log.txt', 'r') as f:
        last = f.readlines()[-1].split()[1]

    with open('log.txt', 'a') as f:
        now = datetime.utcnow()

        if sys.argv[1] == last:
            f.write('{0}-{1}-{2} ..\n'.format(now.year, now.month, now.day))
        else:
            script = __import__(argv)
            f.write('{0}-{1}-{2} {3} {4}\n'.format(now.year, now.month, now.day,
                sys.argv[1], script.__doc__))

        for argv in sys.argv[2:]:
            script = __import__(argv)
            f.write('{0}-{1}-{2} {3} {4}\n'.format(now.year, now.month, now.day,
                sys.argv[1], script.__doc__))
