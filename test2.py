import json

with open('sample.json') as f:
    data = json.load(f)

block = data['blocks']
print(block)