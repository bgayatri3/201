import json
import random

with open("chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

print(f"Loaded {len(chunks)} chunks\n")

for chunk in random.sample(chunks, min(5, len(chunks))):
    print("=" * 80)
    print(f"ID: {chunk['id']}")
    print(f"Source: {chunk['source_file']}")
    print(f"Length: {chunk['n_chars']} chars")
    print("-" * 80)
    print(chunk["text"])
    print("\n")