import os
import random

from music21 import converter
from music21.chord import Chord
from music21.note import Note
from music21.pitch import Pitch
from music21.tree.trees import ElementTree

import graphics
from transpose import transpose

_SONG_DIR_PATH = "/Users/mknutsen/Library/Mobile Documents/com~apple~CloudDocs/ableton_workspace/sample/midi scales"
_SONG_TITLES = ['Phrygian_dominant_scale_on_C.mid', 'Ionian_mode_C.mid', 'Harmonic_major_scale_C.mid',
                'Blues_scale_common.mid', 'Hirajoshi_scale_on_C_Kostka-Payne_%26_Speed.mid',
                'Double_harmonic_scale_quarter_tones.mid', 'Diatonic_scale_on_C_sopranino_clef.mid',
                'Symmetrical_four-semitone_tritone_scale_on_C.mid', 'Enigmatic_scale_on_C_descending.mid',
                'Minor_scale_on_C.mid', 'Diatonic_scale_on_C_tenuto.mid', 'Half_diminished_scale_C.mid',
                'Harmonic_minor_on_C.mid', 'Locrian_mode_C.mid', 'Neapolitan_minor_scale_on_C.mid',
                'Insen_scale_on_C.mid', 'Slendro_on_C.mid', 'Ukrainian_Dorian_mode_on_C.mid',
                'Double_harmonic_scale.mid', 'Diatonic_scale_on_C_legato.mid', 'Gypsy_minor_scale.mid',
                'Chromatic_scale_ascending_on_C.mid', 'Pythagorean_diatonic_scale_on_C.mid', 'C_major_scale.mid',
                'Vietnamese_scale_of_harmonics_on_C.mid', 'Prometheus_scale_on_C.mid',
                'Two-semitone_tritone_scale_on_C.mid', 'Phrygian_mode_C.mid.mp3',
                'Hirajoshi_scale_on_C_Sachs_%26_Slonimsky.mid', 'Lydian_dominant_C.mid', 'Ionian.MID',
                'Augmented_scale_on_C.mid', 'Chromatic_scale_descending_on_C.mid', 'Double_harmonic_scale_on_C.mid',
                'C_harmonic_minor_scale_ascending_and_descending.mid', 'Bebop_dominant_scale_on_C.mid',
                'Lydian_mode_C_midi.mid', 'C_minor_pentatonic_scale.mid', 'Hungarian_gypsy_scale_C.mid',
                'Diatonic_scale_on_C_staccatissimo.mid', 'Diatonic_scale_on_C_marcato.mid',
                'Diatonic_scale_on_C_bass_clef.mid', 'Neapolitan_major_scale_on_C.mid',
                'Slendro_vs_whole_tone_scale_on_C.mid', '13-limit_just_decatonic_scale_on_C.mid',
                'Tritone_scale_on_C.mid', 'Lydian_augmented_scale_on_C.mid', 'Aeolian_mode_C.mid',
                'Diatonic_scale_on_C.mid', 'Major_bebop_scale_on_C.mid', 'Hirajoshi_scale_on_C_Burrows.mid',
                'Istrian_mode_on_C.mid', 'Diatonic_scale_on_C_tablature.mid', 'Major_scale_on_C.mid',
                'Mixolydian_mode_C.mid', 'Thai_pentatonic_scale_mode_1.mid', 'Major_locrian_C.mid',
                'C-natural_major.mid', 'Hungarian_major_scale_on_C.mid', 'Persian_scale_on_C.mid', 'Algerian_scale.mid',
                'Scale_of_harmonics_on_C.mid', 'Altered_scale_on_C.mid', 'Diatonic_scale_on_C_staccato.mid',
                'Enigmatic_scale_on_C.mid', 'Octatonic_scales_on_C.mid', 'Melodic_minor_ascending_on_C.mid']

keyDetune = []
for i in range(0, 127):
    keyDetune.append(random.randint(-30, 30))
song_file_path = os.path.join(_SONG_DIR_PATH, _SONG_TITLES[random.randint(0, len(_SONG_TITLES))])
print(song_file_path)
b = converter.parse(song_file_path)
key = b.analyze('key')  # correlatin coefficient
print("before transpose")
print(f"tonic.name: {key.tonic.name}, mode:{key.mode}, correlationCoefficient:{key.correlationCoefficient}")
b = transpose(b)
key = b.analyze('key')
print("after transpose")
print(f"tonic.name: {key.tonic.name}, mode:{key.mode}, correlationCoefficient:{key.correlationCoefficient}")
tree: ElementTree = b.asTree(flatten=True, classList=[Note, Chord])
lowest_note = Pitch("C8")
highest_note = Pitch("C0")
for x in tree:
    pitches = []
    if isinstance(x, Note):
        pitches = [x.pitch, ]
        pass
    if isinstance(x, Chord):
        pitches = x.pitches

    for note in pitches:
        if note < lowest_note:
            lowest_note = note
        if note > highest_note:
            highest_note = note
print(f"lowest_note: {lowest_note}, lowest_note: {highest_note}")

graphics.main(tree, lowest_note, highest_note)
