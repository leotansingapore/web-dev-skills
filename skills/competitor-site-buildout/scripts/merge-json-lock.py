#!/usr/bin/env python3
"""Resolve a rebase conflict in a generated JSON lock/manifest (e.g. og-cards.lock.json)
by deep-merging BOTH sides' keys. Usage, during a conflicted rebase:
  python3 merge-json-lock.py path/to/file.json && git add path/to/file.json
Side 2 (:2, ours/upstream during rebase) is the base; side 3 (:3, the commit being
replayed) wins on the same key, since it is the newer write for that page."""
import json, subprocess, sys
path = sys.argv[1]
a = json.loads(subprocess.check_output(['git', 'show', f':2:{path}']))
b = json.loads(subprocess.check_output(['git', 'show', f':3:{path}']))
def merge(x, y):
    if isinstance(x, dict) and isinstance(y, dict):
        out = dict(x)
        for k, v in y.items():
            out[k] = merge(x[k], v) if k in x else v
        return out
    return y
with open(path, 'w') as f:
    json.dump(merge(a, b), f, indent=2)
    f.write('\n')
