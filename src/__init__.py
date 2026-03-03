from .Connection import Connection
from .Hub import Hub
from .Map import Map
from .parser import get_data, check_data
import sys
import os

# clean advertisement of pygame
stdout_backup = sys.stdout
sys.stdout = open(os.devnull, 'w')
import pygame as pg # noqa 402
sys.stdout.close()
sys.stdout = stdout_backup

__all__ = [
    'Connection', 'Hub', 'Map',
    'get_data', 'check_data',
    'pg'
]

W_SIZE = (1920, 1080)
SCALE = 3
L_SIZE = (W_SIZE[0] * SCALE, W_SIZE[1] * SCALE)

# color
BG_C = (18, 18, 25)
LINE_c = (90, 90, 110)
START_c = (80, 220, 120)
HUB_c = (80, 140, 255)
GOAL_c = (240, 80, 80)
