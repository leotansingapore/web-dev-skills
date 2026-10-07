#!/usr/bin/env python3
"""Resolve conflicts in an array of route OBJECTS (e.g. marketing-routes.mjs) where both
sides inserted a new `{ ... }` entry at the same spot, so git splits one object across the
hunk. Keeps both entries whole by closing HEAD's object before the replayed one. The CLOSE
string must match the file's object ending: pass it as argv[2] (default below matches
entries ending in "fit: 'cover',\n  },\n  {\n"). Verify by importing the module after.
  python3 merge-route-objects.py scripts/marketing-routes.mjs && git add ..."""
import re, sys
p = sys.argv[1]
close = sys.argv[2].encode().decode('unicode_escape') if len(sys.argv) > 2 else "    fit: 'cover',\n  },\n  {\n"
s = open(p).read()
s = re.sub(r"<<<<<<< [^\n]*\n(.*?)=======\n(.*?)>>>>>>> [^\n]*\n",
           lambda m: m.group(1) + close + m.group(2), s, flags=re.S)
open(p, 'w').write(s)
