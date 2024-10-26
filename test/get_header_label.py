import json

with open('header_label.json', 'r') as f:
    header_label = json.load(f)

print(header_label)