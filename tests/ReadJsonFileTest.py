import json

# read file
with open("Test1"+".json", 'r') as t:
    data = t.read()

# parse file
test = json.loads(data)
code = '\n'.join(test['code'])
print(f"{code}")