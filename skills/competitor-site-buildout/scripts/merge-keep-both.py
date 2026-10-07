#!/usr/bin/env python3
"""Resolve conflicts in LIST-LIKE files (route lists, smoke-test route arrays, hub card
arrays, nav link arrays, import lists) by keeping both sides in order: HEAD's lines, then
the replayed commit's. Only for files where each conflict hunk is independent entries.
Check the result (type-check, tests) and de-duplicate if both sides added the same entry.
  python3 merge-keep-both.py path && git add path"""
import re, sys
p = sys.argv[1]
s = open(p).read()
s = re.sub(r"<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n",
           lambda m: m.group(1) + m.group(2), s, flags=re.S)
open(p, 'w').write(s)
