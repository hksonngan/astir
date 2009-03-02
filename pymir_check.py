#!/usr/bin/env python
from sys import stdout as info

# based
info.write('Loading libraries:\n')
info.write('string.........')
try:
    import string
    info.write('[ok]\n')
except:
    info.write('[E]\n')

info.write('os.............')
try:
    import os
    info.write('[ok]\n')
except:
    info.write('[E]\n')

info.write('sys............')
try:
    import sys
    info.write('[ok]\n')
except:
    info.write('[E]\n')

info.write('math...........')
try:
    import math
    info.write('[ok]\n')
except:
    info.write('[E]\n')

info.write('random.........')
try:
    import random
    info.write('[ok]\n')
except:
    info.write('[E]\n')

info.write('copy...........')
try:
    import copy
    info.write('[ok]\n')
except:
    info.write('[E]\n')

info.write('Tkinter........')
try:
    import Tkinter
    info.write('[ok]\n')
except:
    info.write('[E]\n')

info.write('PIL............')
try:
    import PIL
    info.write('[ok]\n')
except:
    info.write('[E]\n')

info.write('ImageDraw......')
try:
    import ImageDraw
    info.write('[ok]\n')
except:
    info.write('[E]\n')

info.write('Image..........')
try:
    import Image
    info.write('[ok]\n')
except:
    info.write('[E]\n')

info.write('Numpy..........')
try:
    import numpy
    info.write('[ok]\n')
except:
    info.write('[E]\n')

