import json
import csv

# Read JSON
with open("prompts.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Write CSV
with open("prompts.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Index", "Prompt"])  # Headers
    for key, value in data.items():
        writer.writerow([key, value])

print("✅ Converted to prompts.csv")
