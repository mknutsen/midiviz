import subprocess
from math import floor
from threading import Thread
from time import time
from typing import Dict, List

import musicalbeeps
import pygame
from mido import second2tick, bpm2tempo
from mido.messages.messages import Message
from music21.chord import Chord
from music21.note import Note
from music21.pitch import Pitch
from music21.stream import Stream
from pygame import Color
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.tests.draw_test import GREEN

_DESIRED_BPM = 40
_TEMPO_MICROSECONDS_PER_BEAT = bpm2tempo(_DESIRED_BPM)
_DEFAULT_TICKS_PER_BEAT = 480
_KEY_VERITCAL_OFFSET = 0
_KEY_HORIZONTAL_OFFSET = 100
_KEY_WIDTH = 40
_KEY_LENGTH_STEP = 60
_KEY_MAX_LENGTH = 800
_SECONDS_PER_MINUTE = 60
_FONT_NAME = "Roboto-Bold.ttf"

_KEY_ORDERING = [Pitch("D3"),
                 Pitch("B2"),
                 Pitch("G2"),
                 Pitch("E2"),
                 Pitch("C2"),
                 Pitch("A1"),
                 Pitch("F1"),
                 Pitch("D1"),
                 Pitch("C1"),
                 Pitch("E1"),
                 Pitch("G1"),
                 Pitch("B1"),
                 Pitch("D2"),
                 Pitch("F2"),
                 Pitch("A2"),
                 Pitch("C3"),
                 Pitch("E3")]


def beats_to_seconds(beats_duration: int):
    # print(_DESIRED_BPM, _SECONDS_PER_MINUTE, beats_duration)
    return  _SECONDS_PER_MINUTE * beats_duration / _DESIRED_BPM


class Key(Sprite):
    def __init__(self, note: str, screen, font):
        self.screen = screen
        Sprite.__init__(self)
        self.note = note
        index = _KEY_ORDERING.index(Pitch(note))
        middle = floor(len(_KEY_ORDERING) / 2)
        self.distance_from_middle = abs(middle - index)
        self.key_length = _KEY_MAX_LENGTH - self.distance_from_middle * _KEY_LENGTH_STEP
        self.image = Surface((_KEY_WIDTH, self.key_length))
        self.rect = self.image.get_rect(topleft=(_KEY_HORIZONTAL_OFFSET + _KEY_WIDTH * index, _KEY_VERITCAL_OFFSET))
        self.state = False
        # self.image.fill((self.distance_from_middle * 100 % 255, 60, 200))
        self.font = font
        self.end_time_sec = 0

    def press(self, duration: int) -> None:
        self.state = True
        self.end_time_sec = duration + floor(time())

    def update(self):
        if self.state and self.end_time_sec < time():
            self.state = False
            self.end_time_sec = 0

        normal_color = (self.distance_from_middle * 100 % 255, 60, 200)
        highlight_color = (102, 255, 0)
        self.image.fill((highlight_color if self.state else normal_color))
        index = _KEY_ORDERING.index(Pitch(self.note))
        img1 = self.font.render(self.note, False, GREEN)
        self.screen.blit(img1, (_KEY_HORIZONTAL_OFFSET + _KEY_WIDTH * index, 50))
        pass


def main(notes: Stream, lowest_note: Pitch, highest_note: Pitch):
    player = musicalbeeps.Player(volume=0.3,
                                 mute_output=False)
    notes_list = list(notes)

    lowest_note_midi = 130
    for key in _KEY_ORDERING:  # try highest and see which covers more
        if lowest_note.name == key.name:
            lowest_note_midi = min(key.midi, lowest_note_midi)
    adjustment = lowest_note.midi - lowest_note_midi
    print(f"midi adjustment to fit on kalimba {adjustment}")

    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))
    _SYS_FONT = pygame.font.SysFont("helvetica", floor(_KEY_WIDTH / 2))
    key_list = [Key(str(key), screen, _SYS_FONT) for key in _KEY_ORDERING]
    key_dict = {Pitch(key.note).midi: key for key in key_list}
    sprites = pygame.sprite.Group(key_list)
    clock = pygame.time.Clock()
    run = True
    begin_sec = time()
    next_note = notes_list.pop(0)
    while run:
        # INSIDE OF THE GAME LOOP
        if not notes_list:
            begin_sec = time()
            notes_list = list(notes)
            next_note = notes_list.pop(0)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False

        screen.fill((0, 0, 0))
        if next_note:
            now_sec = time()
            time_since_begin_sec = now_sec - begin_sec

            tics = second2tick(time_since_begin_sec, _DEFAULT_TICKS_PER_BEAT, _TEMPO_MICROSECONDS_PER_BEAT)
            # print(tics, next_note.midiTickStart)
            while next_note and next_note.midiTickStart <= tics:
                duration_seconds = beats_to_seconds(next_note.duration.quarterLength)
                print("hey", next_note, next_note.duration)
                pitches = []
                if isinstance(next_note, Note):
                    pitches = [next_note.pitch, ]

                if isinstance(next_note, Chord):
                    pitches = next_note.pitches

                for note in pitches:
                    Thread(target=player.play_note, args=[str(note), duration_seconds]).start()
                    try:
                        key_dict[note.midi - adjustment].press(
                            duration_seconds)
                    except Exception as e:
                        print(note, note.midi, adjustment, e)
                # begin_sec = time()
                next_note = notes_list.pop(0) if notes_list else None

        sprites.draw(screen)
        sprites.update()
        pygame.display.flip()
        clock.tick()
