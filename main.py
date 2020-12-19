from typing import Dict

import mido

import graphics

_IMAGE_PATH = "/Users/mknutsen/Documents/GitHub/midiviz/pic.png"
_SONG_FILE_PATH = "/Users/mknutsen/Library/Mobile Documents/com~apple~CloudDocs/ableton_workspace/sample/Wii Channels - Mii Channel.mid"
_NOTE_ON = "note_on"
mid = mido.MidiFile(_SONG_FILE_PATH)

# print(mid.tracks)

notes_in_song = [note for note in mid.tracks[1] if note.type == _NOTE_ON]
highest = 0
lowest = 99999999999999
for note in notes_in_song:
    lowest = min(note.note, lowest)
    highest = max(note.note, highest)

print(lowest, highest)
graphics.main(notes_in_song)
