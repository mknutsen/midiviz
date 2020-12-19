from math import floor
from time import time
from typing import List, Dict

import musicalbeeps
import pygame

from pygame import Color

from mido.messages.messages import Message
from mido import second2tick
from pygame.sprite import Sprite
from pygame.surface import Surface
from pygame.tests.draw_test import GREEN

_DEFAULT_TEMPO = 200000
_DEFAULT_TICKS_PER_BEAT = 480
_KEY_VERITCAL_OFFSET = 0
_KEY_HORIZONTAL_OFFSET = 100
_KEY_WIDTH = 40
_KEY_LENGTH_STEP = 60
_KEY_MAX_LENGTH = 800
_FONT_NAME = "Roboto-Bold.ttf"

_midi_conversion_table: Dict[int, str] = {
    127: "G9",
    126: "F9#",
    125: "F9",
    124: "E9",
    123: "D9#",
    122: "D9",
    121: "C9#",
    120: "C9",
    119: "B8",
    118: "A8#",
    117: "A8",
    116: "G8#",
    115: "G8",
    114: "F8#",
    113: "F8",
    112: "E8",
    111: "D8#",
    110: "D8",
    109: "C8#",
    108: "C8",
    107: "B7",
    106: "A7#",
    105: "A7",
    104: "G7#",
    103: "G7",
    102: "F7#",
    101: "F7",
    100: "E7",
    99: "D7#",
    98: "D7",
    97: "C7#",
    96: "C7",
    95: "B6",
    94: "A6#",
    93: "A6",
    92: "G6#",
    91: "G6",
    90: "F6#",
    89: "F6",
    88: "E6",
    87: "D6#",
    86: "D6",
    85: "C6#",
    84: "C6",
    83: "B5",
    82: "A5#",
    81: "A5",
    80: "G5#",
    79: "G5",
    78: "F5#",
    77: "F5",
    76: "E5",
    75: "D5#",
    74: "D5",
    73: "C5#",
    72: "C5",
    71: "B4",
    70: "A4#",
    69: "A4",
    68: "G4#",
    67: "G4",
    66: "F4#",
    65: "F4",
    64: "E4",
    63: "D4#",
    62: "D4",
    61: "C4#",
    60: "C4",
    59: "B3",
    58: "A3#",
    57: "A3",
    56: "G3#",
    55: "G3",
    54: "F3#",
    53: "F3",
    52: "E3",
    51: "D3#",
    50: "D3",
    49: "C3#",
    48: "C3",
    47: "B2",
    46: "A2#",
    45: "A2",
    44: "G2#",
    43: "G2",
    42: "F2#",
    41: "F2",
    40: "E2",
    39: "D2#",
    38: "D2",
    37: "C2#",
    36: "C2",
    35: "B1",
    34: "A1#",
    33: "A1",
    32: "G1#",
    31: "G1",
    30: "F1#",
    29: "F1",
    28: "E1",
    27: "D1#",
    26: "D1",
    25: "C1#",
    24: "C1",
    23: "B0",
    22: "A0#",
    21: "A0",
    20: "&nbsp;",
    19: "&nbsp;",
    18: "&nbsp;",
    17: "&nbsp;",
    16: "&nbsp;",
    15: "&nbsp;",
    14: "&nbsp;",
    13: "&nbsp;",
    12: "&nbsp;",
    11: "&nbsp;",
    10: "&nbsp;",
    9: "&nbsp;",
    8: "&nbsp;",
    7: "&nbsp;",
    6: "&nbsp;",
    5: "&nbsp;",
    4: "&nbsp;",
    3: "&nbsp;",
    2: "&nbsp;",
    1: "&nbsp;",
    0: "&nbsp;", }

_KEY_ORDERING = ["D3",
                 "B2",
                 "G2",
                 "E2",
                 "C2",
                 "A1",
                 "F1",
                 "D1",
                 "C1",
                 "E1",
                 "G1",
                 "B1",
                 "D2",
                 "F2",
                 "A2",
                 "C3",
                 "E3", ]


class Explosion(Sprite):
    def __init__(self, pos):
        Sprite.__init__(self)
        self.image = Surface((60, 60))
        self.rect = self.image.get_rect(center=pos)
        self.state = 0

    def update(self):
        self.state += 1
        self.image.fill((0, 0, 0))
        pygame.draw.circle(self.image, (200, 5 * self.state, 0), self.image.get_rect().center, self.state)
        if self.state > 30:
            self.kill()


class Key(Sprite):
    def __init__(self, note: str, screen, font):
        self.screen = screen
        Sprite.__init__(self)
        self.note = note
        index = _KEY_ORDERING.index(note)
        middle = floor(len(_KEY_ORDERING) / 2)
        self.distance_from_middle = abs(middle - index)
        self.key_length = _KEY_MAX_LENGTH - self.distance_from_middle * _KEY_LENGTH_STEP
        self.image = Surface((_KEY_WIDTH, self.key_length))
        self.rect = self.image.get_rect(topleft=(_KEY_HORIZONTAL_OFFSET + _KEY_WIDTH * index, _KEY_VERITCAL_OFFSET))
        self.state = False
        # self.image.fill((self.distance_from_middle * 100 % 255, 60, 200))
        self.font = font

    def update(self):
        normal_color = (self.distance_from_middle * 100 % 255, 60, 200)
        highlight_color = (102, 255, 0)
        self.image.fill((highlight_color if self.state else normal_color))
        index = _KEY_ORDERING.index(self.note)
        img1 = self.font.render(self.note, False, GREEN)
        self.screen.blit(img1, (_KEY_HORIZONTAL_OFFSET + _KEY_WIDTH * index, 50))
        pass


class Ball(Sprite):
    def __init__(self, pos, screen):
        Sprite.__init__(self)
        self.image = Surface((40, 40))
        self.image.fill((60, 60, 200))
        self.rect = self.image.get_rect(center=pos)
        self.dir = 3
        self.screen = screen

    def update(self):
        if not self.screen.get_rect().contains(self.rect):
            self.dir *= -1
        self.image.fill((self.rect.x % 255, 60, 200))
        self.rect.move_ip(self.dir, 0)


def main(notes: List[Message]):
    player = musicalbeeps.Player(volume=0.3,
                                 mute_output=False)
    print(notes)
    pygame.init()
    screen = pygame.display.set_mode((1000, 1000))
    _SYS_FONT = pygame.font.SysFont("helvetica", floor(_KEY_WIDTH / 2))
    key_list = [Key(key, screen, _SYS_FONT) for key in _KEY_ORDERING]
    key_dict = {key.note: key for key in key_list}
    sprites = pygame.sprite.Group(key_list)
    clock = pygame.time.Clock()
    run = True
    begin_sec = time()
    next_note: Message = notes.pop(0)
    last_played = None
    while run:
        # INSIDE OF THE GAME LOOP
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                sprites.add(Explosion(e.pos))

        screen.fill((0, 0, 0))
        if notes:
            now_sec = time()
            time_since_begin_sec = now_sec - begin_sec
            tics = second2tick(time_since_begin_sec, _DEFAULT_TICKS_PER_BEAT, _DEFAULT_TEMPO)
            if next_note.time <= tics:
                player.play_note(_midi_conversion_table[next_note.note], 0.5)
                try:
                    note_number = next_note.note - 12 * 3
                    note_letter = _midi_conversion_table[note_number]
                    if last_played:
                        last_played.state = False
                    last_played = key_dict[note_letter]
                    last_played.state = True
                except Exception as e:
                    print(e)
                begin_sec = time()
                next_note = notes.pop(0)

        sprites.draw(screen)
        sprites.update()
        pygame.display.flip()
        clock.tick(20)
