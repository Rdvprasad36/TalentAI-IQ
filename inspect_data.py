import orjson
from pprint import pprint

with open("data/candidates.jsonl", "rb") as f:
    candidate = orjson.loads(f.readline())

print("=" * 80)
print("TOP LEVEL KEYS")
print("=" * 80)
print(candidate.keys())

print("\n")
print("=" * 80)
print("FULL FIRST CANDIDATE")
print("=" * 80)

pprint(candidate, width=120)