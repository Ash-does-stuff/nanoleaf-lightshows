from nanoleafapi import Nanoleaf, NanoleafDigitalTwin
import socket
import json
from time import sleep
from random import randint
import struct
import re

hex_re = r"[a-fA-F0-9]{6}"

nanoleaf_host = 'YOUR NANOLEAF IP'
nanoleaf_udp_port = 60222

nanoleaf_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)

nl = Nanoleaf(nanoleaf_host)
nl.enable_extcontrol()

ids = nl.get_ids()
ids.pop(len(ids)-1)

random_id_arr = []
random_id_arr = ids.copy()

class Color:
    def __init__(self,r,g,b,w):
        self.r = r
        self.g = g
        self.b = b
        self.w = w


colors = {
            "black": Color(0,0,0,0),
            "grey": Color(127,127,127,0),
            "white": Color(255,255,255,0),
            "red": Color(255,0,0,0),
            "green": Color(0,255,0,0),
            "blue": Color(0,0,255,0),
        }


class PanelState:
    def __init__(self, id, color, transition):
        self.panel_id = id
        self.color = color
        self.transition = transition


class Event:
    def __init__(self,time,panel_states):
        self.time = time
        self.panel_states = panel_states

    def add_panel_state(self,panel_state):
        self.panel_states[str(panel_state.panel_id)] = panel_state




def create_panel_data(panel_ids):
    important_panels = {}
    for id in panel_ids:
        important_panels[id] = False
    return {
        "ids_random": ids.copy(),
        "important_panels": important_panels
    }


def check_color(action):
    color = action["color"]
    result = ""
    if color in colors.keys():
        result = colors[color]
    elif re.search(hex_re,color):
            temp = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
            result = Color(temp[0],temp[1],temp[2],0)
    else:
        raise Exception("Invalid color at action " + str(action))
    return result


def check_id(action,ids_random):
    id = 0       
    if action["panel_id"] in ids:
        id = action["panel_id"]
    elif action["panel_id"] == "RAND":
        i = randint(0,len(ids_random)-1)
        id = ids_random.pop(i)
    else:
        raise Exception("Invalid id value at action " + str(action))
    return id


def process_action(action, panel_data):
    result = []

    important = False
    try:
        print("haaaa")
        important = action["important"]
    except:
        print("no important value, skipping")

    match action["action"]:
        case "light":
            color = check_color(action)
            id = check_id(action, panel_data["ids_random"])
            
            panel_data["important_panels"][id] = important

            result.append(PanelState(id,color,action["transition"]))

        case "set":
            color = check_color(action)

            for id in ids:
                if important:
                    panel_data["important_panels"][id] = False

                if not panel_data["important_panels"][id]:
                    result.append(PanelState(id,color,action["transition"]))
                

    return result


def translate_panel_state_to_bytes(panel_state):
    result = b""

    result += panel_state.panel_id.to_bytes(2, "big")
    result += panel_state.color.r.to_bytes(1, "big")
    result += panel_state.color.g.to_bytes(1, "big")
    result += panel_state.color.b.to_bytes(1, "big")
    result += panel_state.color.w.to_bytes(1, "big")
    result += panel_state.transition.to_bytes(2, "big")

    return result


def process_file(data):
    panel_data = create_panel_data(ids)

    events = []
    time = 0
    tempEvent = Event(time,{})
    for action in data["actions"]:
        if action["time"] != time:
            events.append(tempEvent)
            time = float(action["time"])
            tempEvent = Event(time,{})
        panel_states = process_action(action, panel_data)
        for state in panel_states:
            tempEvent.add_panel_state(state)
    events.append(tempEvent)

    events.sort(key=(lambda event : event.time))

    sleep(data["metadata"]["offset"]/1000)
    play_lightshow(events)


def play_lightshow(events):
    for i in range(len(events)):
        currentEvent = events[i]

        if currentEvent.panel_states != {}:
            active_panels = currentEvent.panel_states.keys()

            send_data = b""
            send_data += (len(active_panels)).to_bytes(2, "big")

            for panel_id in active_panels:
                send_data += translate_panel_state_to_bytes(currentEvent.panel_states[panel_id])

            nanoleaf_socket.sendto(send_data, (nanoleaf_host, nanoleaf_udp_port))
        
        try:
            nextEvent = events[i+1]
            sleep((nextEvent.time - currentEvent.time)*beatInMs)
        except:
            print("lightshow ended")


f = open('pharmacy-converted.json')
data = json.load(f)

bpm = data["metadata"]["bpm"]
beatInMs = 60/bpm
print(ids)
process_file(data)




