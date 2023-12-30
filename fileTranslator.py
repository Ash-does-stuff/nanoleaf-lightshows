import json

fileName = "test"
timeOffset = 0

changeTime = False
changeIDs = True

file = open(fileName + ".json", "r")
fileJson = json.loads(file.read())

dictionary = fileJson["dictionary"]

for action in fileJson["actions"]:
    if changeTime:
        action["time"] = float(action["time"]) + timeOffset
    if changeIDs and action["action"] != "set" and action["panel_id"] != "RAND":
        action["panel_id"] = dictionary[action["panel_id"]]

fileJson["actions"].sort(key=(lambda action : action["time"]))

f = open(fileName + "-converted.json", "w")
f.write(json.dumps(fileJson))