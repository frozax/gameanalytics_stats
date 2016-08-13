#́!/usr/bin/env python
import sys

from clientdata import client_data_generator

f = sys.argv[1]
nbc = 0
cdg = client_data_generator(f)
for c in cdg:
    c.compute_stats()
    print(c)
    nbc += 1
    if nbc > 5:
        break
