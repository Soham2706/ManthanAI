import json

with open("../data/sample_candidates.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("Type:", type(data))

if isinstance(data, list):
    print("Number of samples:", len(data))
    print("\nFirst Candidate:\n")
    print(json.dumps(data[0], indent=2))
else:
    print(json.dumps(data, indent=2))