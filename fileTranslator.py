import json

fileName = "handCrushed"
timeOffset = 0

dictionary = {
    "a": 34881,
    "b": 64611,
    "c": 40291,
    "d": 24026,
    "e": 3467,
    "f": 8174,
    "g": 35662,
    "h": 19806,
    "i": 58321,
    "j": 38274,
    "k": 16905,
    "l": 16322,
    "m": 63080,
    "n": 50002,
    "o": 40125
}

file = open(fileName + ".json", "r")
fileJson = json.loads(file.read())

for action in fileJson["actions"]:
    action["time"] = float(action["time"]) + timeOffset
    if action["action"] != "set":
        action["panel_id"] = dictionary[action["panel_id"]]

f = open(fileName + "-converted.json", "w")
f.write(json.dumps(fileJson))