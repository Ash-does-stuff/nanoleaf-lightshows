import json

fileName = "handCrushed"
timeOffset = 0

dictionary = {
    "a": "34881",
    "b": "64611",
    "c": "40291",
    "d": "24026",
    "e": "3467",
    "f": "8174",
    "g": "35662",
    "h": "19806",
    "i": "58321",
    "j": "38247",
    "k": "16905",
    "l": "16322",
    "m": "63080",
    "n": "50002",
    "o": "40125"
}

file = open(fileName + ".json", "r")
text = json.load(file.read())

for action in text["actions"]:
    action["time"] = action["time"] + timeOffset
    action["panel_id"] = dictionary[action["panel_id"]]

print(text)

f = open(fileName + "-converted.json", "w")
f.write(text)