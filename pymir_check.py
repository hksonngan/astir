#!/usr/bin/env python
#
# This file is part of Astir
# 
# Astir is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Astir is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Astir.  If not, see <http://www.gnu.org/licenses/>.
#
# Astir Copyright (C) 2008 Julien Bert 

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

info.write('ctypes.........')
try:
    import ctypes
    info.write('[ok]\n')
except:
    info.write('[E]\n')

info.write('pylibtiff......')
try:
    import libtiff
    info.write('[ok]\n')
except:
    info.write('[E]\n')

info.write('Numpy..........')
try:
    import numpy
    info.write('[ok]\n')
except:
    info.write('[E]\n')

info.write('Scipy..........')
try:
    import scipy
    info.write('[ok]\n')
except:
    info.write('[E]\n')

info.write('Matplotlib.....')
try:
    import matplotlib
    info.write('[ok]\n')
except:
    info.write('[E]\n')

info.write('FFmpeg.........')
import commands
res = commands.getoutput('ffmpeg -version')
if res.find('version') != -1:
    #res = res.split('\n')[0]
    #res = res.split()
    #info.write('[ok] version %s\n' % res[2])
    info.write('[ok]\n')
else:
    info.write('[E]\n')


