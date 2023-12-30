# nanoleaf-lightshows
Lets you create light shows for Nanoleaf products :3 (I hope)

## Setup
Create an empty JSON file and in it, paste this template:
```json
{
    "metadata": {
        "bpm": 60.0,
    },
    "dictionary":  {},
    "actions": []
}
```
### Metadata
The only important value here is the BPM. This is what the timing of your actions is tied to. 
If you aren't charting a light show for a song, set the BPM to 60, so that 1 beat equals 1 second.

You can also add any other values you wish here, for example, the chart's author or the song the light show is charted to.
### Dictionary
Here you can set aliases for your Nanoleaf panel IDs. 
These can be used for the panel_id value of an action instead of an actual panel ID.
Example:
```json
"dictionary":  {
        "a": 34881,
        "b": 64611,
        "c": 40291,
        "d": 24026,
    }
```
*Charts that use aliases have to be translated using ``fileTranslator.py``.
### Actions
This is where the "actions" are located. Actions are what actually make the panels light up.
An action has to have these values:
- time
    - The time in beats when the action should happen.
    - The length of a beat is tied to the BPM value that was set previously in the metadata.
- action
    - The type of the action
    - light
        - Lights up one individual panel.
        - Actions with this type require an extra ``panel_id`` value.
    - set
        - Light up all available panels.
- color
    - The color in which the panel/s should light up.
    - Can either be a hex string or one of the color names below
        - ``black`` (the panel is turned off), ``grey``, ``white``, ``red``, ``green``, ``blue``
- transition
    - The time it takes to transition from the previous panel state to this one.
    - Is an integer larger or equal to one.
    - 1 = 100ms, 2 = 200ms.
- panel_id
    - Only required when the action has the ``light`` type.
    - The ID of the target panel.
    - Can either be the ID of a Nanoleaf panel, one of the aliases set in the ``dictionary`` value, or "RAND", which lights up a random available panel.

An example of a ``set`` and a ``light`` action:
```json
        {
            "time": "0",
            "action": "set",
            "color": "black",
            "transition": 1
        },
        {
            "time": "4",
            "action": "light",
            "color": "ff00ff",
            "transition": 10,
            "panel_id": "RAND"
        }
```

