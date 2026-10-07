#!/usr/bin/env python3
"""Rank feature gaps by whether the product's daily users would want them. Jev decides.

Ranking gaps is a decision, and decisions go to Jev (TypeSafe), not an LLM prompt. This
asks one yes/no question per gap and prints the gaps surest-first. Facts still override
it: a gap the target's transport cannot do, or one the owner decided against, stays out
whatever it scores.

    TYPESAFE_API_KEY=... rank_gaps.py gaps.json

gaps.json:
    {"product": "<what it is, WHO uses it daily and for what, transport limits>",
     "gaps": [{"id": "g7", "feature": "<the missing capability, phrased as what a user could do>"}]}

The `product` line matters most: with only a name, developer-facing gaps (webhooks, BYO
keys) score as high as daily-use ones. No key or Jev down: prints the list unranked.
"""
import json
import os
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

MODEL = "jev-1.13.0"  # pinned: a model change has to be a decision
ENDPOINT = "https://api.typesafe.ai/v1/systemone"

Q = {
    "type": "noul",
    "instructions": "Would the people described in `product`, using it every day, notice and want the missing capability in `feature` if it were added?",
    "criteria": {
        "true": "It saves them time on a task they do often, stops a mistake or a lost lead or sale, or lets them do something they currently cannot and would ask for.",
        "false": "It mainly serves developers, self-hosters or integrators, duplicates something they already have another way, or is a cosmetic preference they would not ask for.",
    },
}


def ask(key, state):
    body = json.dumps({"model": MODEL, "state": state, "questions": {"q": Q}}).encode()
    for attempt in range(3):
        try:
            req = urllib.request.Request(ENDPOINT, data=body, headers={
                "Authorization": "Bearer " + key, "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=25) as res:
                return float(json.load(res)["answers"]["q"]["noul"])
        except Exception:  # noqa: BLE001 - retry, then report the gap unscored
            time.sleep(2 * (attempt + 1))
    return None


def main():
    data = json.load(open(sys.argv[1]))
    gaps = data["gaps"]
    key = os.environ.get("TYPESAFE_API_KEY")
    scores = {}
    if key:
        with ThreadPoolExecutor(5) as pool:
            got = pool.map(lambda g: ask(key, {"product": data["product"], "feature": g["feature"]}), gaps)
            scores = {g["id"]: s for g, s in zip(gaps, got) if s is not None}
    if not scores:
        for g in gaps:
            print(f"  n/a  {g['id']}  {g['feature']}")
        print("\n(unranked: " + ("Jev gave no answers" if key else "no TYPESAFE_API_KEY") + ")", file=sys.stderr)
        return 0
    for g in sorted(gaps, key=lambda g: -scores.get(g["id"], -1.0)):
        s = scores.get(g["id"])
        print(f"{'  n/a' if s is None else f'{s:5.2f}'}  {g['id']}  {g['feature']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
