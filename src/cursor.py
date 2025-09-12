import pygame

from obj import Obj
from global_functions import *

class Cursor(Obj):
    def __init__(self, x, y):
        # DIRECTION, ANIMATION TIME, FRAME TIME, AND PROBABLY TILE SIZE ARE USELESS FOR THIS
        # SO I DEFAULTED THEM
        anim_stack = []
        img = "/Users/royhouwayek/Documents/WorkSpaces/pyTutor/game2d/img/_10/gold_10.png"
        super().__init__(x, y, TILE_SIZE, "u", 1, 1, img, anim_stack, False)
        self.is_cursor = 1