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

#  Created by Julien Bert on 05/11/08.

## IMAGE ####################
# V0.1 2008-11-30 23:00:30 JB 
# V0.2 2009-03-31 20:32:03 JB
def image_read(name):
    '''
    Read an image from file, return PIL data.
    => [name] image filename (png, bmp or jpg)
    <= im     PIL image data
    '''
    import string, os, Image, sys

    # I assume the checkin is done at the top level
    #
    # check entry
    #listext = ['png', 'bmp', 'jpg']
    #ext     = string.lower(name.split('.')[-1])
    #if ext not in listext:
    #        print 'The image file must be %s format.' % listext
    #        sys.exit()

    # read image
    try:
            im = Image.open(name)
    except IOError:
            print 'Impossible to read the file %s.' % name
            sys.exit()

    return im

# V0.1 2008-12-07 00:14:56 JB 
def image_write(im, name):
    '''
    Write PIL image data to file format
    => [im]   PIL image data
    => [name] Filename to export the image (might be png, bmp or jpg)
    <= nothing
    '''
    import string, Image, sys

    if len(name.split('.')) < 2:
        print 'Filename without extension!'
        sys.exit()

    # check entry
    listext = ['png', 'bmp', 'jpg']
    ext     = string.lower(name.split('.')[-1])
    if ext not in listext:
        print 'The image file must be %s format.' % listext
        sys.exit()

    # write image
    try:
        im.save(name)
    except IOError:
        print 'Impossible to write the file %s.' % name
        sys.exit()

"""
# V0.1 2009-03-06 16:46:29 JB
def image_show_grid(image, dgrid, color = 'red'):
    '''
    Display PIL image data to window Tkinter form, and draw
    a grid with an interspace define byd dgrid.
    => [image] PIL image data
    => [dgrid] Interspace of the grid
    => <color> Link color: 'black', 'red', 'green', 'white' or 'blue'
               (default red)
    <= nothing
    '''
    from numpy import array

    # define grid
    h, w   = image.size
    l1, l2 = [], []
    for y in xrange(0, w, dgrid):
        l1.append([y,     0])
        l2.append([y, h - 1])
    for x in xrange(0, h, dgrid):
        l1.append([0,     x])
        l2.append([w - 1, x])
    l1 = array(l1)
    l2 = array(l2)
    image = image_plot_lines(image, l1, l2, color)
    image_show(image)
"""

# V0.1 2009-08-25 10:02:07 JB
class win:
    def __init__(self):
        from Tkinter import Tk, Canvas
        self.win  = Tk()
        self.bmp  = None
        self.item = None
        self.im   = None

    def surf(self, wmax, hmax):
        from Tkinter import Canvas
        self.surf = Canvas(self.win, width = wmax, height = hmax, bg = 'white')
        self.surf.pack(side = 'left')

    def update(self):
        from PIL import ImageTk, Image
        if self.im is not None:
            self.bmp  = ImageTk.PhotoImage(self.im)
            self.item = self.surf.create_image(0, 0, image = self.bmp, anchor='nw')

    def fit(self, image, wmax, hmax):
        w, h = image.size
        r    = w / float(h)
        flag = False
        if w > wmax:
            w = wmax
            h = int(w / r)
            flag = True
            print 'too large'
        if h > hmax:
            h = hmax
            w = int(h * r)
            flag = True
            print 'too high'
        
        if flag:
            image = image.resize((w, h)) # default nearest
            
        return image, w, h

# V0.1 2008-11-30 23:11:38 JB
# V0.2 2009-08-25 09:25:17 JB
# V0.3 2009-08-26 13:08:58 JB
def image_show(images):
    '''
    Display PIL images data to window Tkinter form.
    => [images] list of PIL images data (no more than 2)
    <= nothing
    '''
    from Tkinter import Tk, Canvas
    from PIL     import ImageTk, Image
    from math    import sqrt, ceil
    import sys

    wmax  = 1280
    hmax  = 600
    mywin = win()

    def one_image(images, wmax, hmax):
        image, w, h = mywin.fit(images[0], wmax, hmax)
        return image, w, h
 
    def two_images(images, wmax, hmax):
        im1, w1, h1 = mywin.fit(images[0], wmax // 2, hmax)
        im2, w2, h2 = mywin.fit(images[1], wmax // 2, hmax)
        wmax        = w1 + w2
        hmax        = max(h1, h2)
        map         = Image.new('RGB', (wmax, hmax), (0, 0, 0))
        dh1         = (hmax - h1) // 2
        map.paste(im1, (0,  dh1, w1, h1 + dh1))
        dh2         = (hmax - h2) // 2
        map.paste(im2, (w1, dh2, w1 + w2, h2 + dh2))

        return map, wmax, hmax
 
    if not isinstance(images, list): images = [images]
    v   = len(images)

    # prepare images
    if   v == 1: map, wmax, hmax = one_image(images,  wmax, hmax)
    elif v == 2: map, wmax, hmax = two_images(images, wmax, hmax)

    # window
    mywin.surf(wmax, hmax)
    mywin.im = map
    mywin.update() 
    mywin.win.mainloop()

global g_p, g_i
# V0.1 2009-03-06 16:26:57 JB
# V0.2 2009-03-27 13:48:27 JB
# V0.3 2009-08-26 15:22:12 JB
def image_show_get_pts(image, nbpts, rad = 35):
    '''
    Display PIL image data to window Tkinter form in order
    to select some points with the mouse.
    => [image] PIL image data
    => [nbpts] Number of points required
    <= [pts]   List of points [[y0, x0], [y1, x1], ..., [yi, xi]]
    '''
    from Tkinter import Tk, Canvas
    from PIL     import ImageTk, Image
    import sys

    global g_p, g_i, g_n
    g_p = []
    g_i = 0
    g_n = nbpts

    wmax  = 1280
    hmax  = 600
    mywin = win()

    def callback(event):
        global g_p, g_i, g_n
        x, y = event.x, event.y
        if g_i < g_n:
            y -= 1 # bordure
            if x < 0:     x = 0
            if y < 0:     y = 0
            if x >= wmax: x = wmax - 1
            if y >= hmax: y = hmax - 1
            g_p.append([y, x])
            g_i += 1
            mywin.im = image_plot_points(mywin.im, g_p, 'win', 'red', rad = rad)
            mywin.update()
        else:
            mywin.win.destroy()

    map, wmax, hmax = mywin.fit(image, wmax, hmax)

    # window
    mywin.surf(wmax, hmax)
    mywin.im  = map
    mywin.update() 
    mywin.surf.bind('<Button-1>', callback)
    mywin.surf.pack()

    mywin.win.mainloop()

    return g_p

global g_p, g_i, g_n
# V0.1 2009-08-25 09:26:16 JB
def image_show_stereo_get_pts(im1, im2, nbpts):
    '''
    Display two PIL images data to window Tkinter form in order
    to select some points with the mouse
    => [im1]    Left PIL image data
    => [im2]    Right PIL image data
    => [nbpts]  Number of points required
    <= [pts]    List of points [[y0, x0], [y1, x1], ..., [yi, xi]] 
    '''
    from Tkinter import Tk, Canvas
    from PIL     import ImageTk, Image
    from math    import sqrt, ceil
    import sys

    global g_p1, g_p2, g_i, g_n
    g_p1 = []
    g_p2 = []
    g_i  = 0
    g_n  = nbpts
    
    wmax  = 1280
    hmax  = 600
    mywin = win()
    
    def two_images(images, wmax, hmax):
        im1, w1, h1 = mywin.fit(images[0], wmax // 2, hmax)
        im2, w2, h2 = mywin.fit(images[1], wmax // 2, hmax)
        wmax        = w1 + w2
        hmax        = max(h1, h2)
        map         = Image.new('RGB', (wmax, hmax), (0, 0, 0))
        dh1         = (hmax - h1) // 2
        map.paste(im1, (0,  dh1, w1, h1 + dh1))
        dh2         = (hmax - h2) // 2
        map.paste(im2, (w1, dh2, w1 + w2, h2 + dh2))

        return map, wmax, hmax, w1, w2, h1, h2, dh1, dh2
 
    def callback(event):
        global g_p1, g_p2, g_i, g_n
        x, y = event.x, event.y

        if g_i < g_n:
            y -= 1 # bordure
            if x < 0:         return
            if y < dh1:       return
            if x >= w1:       return
            if y >= h1 + dh1: return
            g_p1.append([y, x])
            g_i += 1
            mywin.im = image_plot_points(mywin.im, g_p1, 'target', 'red', 1)
            mywin.update()
        elif g_i < 2 * g_n:
            y -= 1 # bordure
            if x < w1:        return
            if y < dh2:       return
            if x >= w1 + w2:  return
            if y >= h2 + dh2: return
            g_p2.append([y, x])
            g_i += 1
            mywin.im = image_plot_points(mywin.im, g_p2, 'target', 'green', 1)
            mywin.update()
        else:        
            mywin.win.destroy()

    # prepare images
    map, wmax, hmax, w1, w2, h1, h2, dh1, dh2 = two_images([im1, im2], wmax, hmax)

    # window
    mywin.surf(wmax, hmax)
    mywin.im  = map
    mywin.update() 
    mywin.surf.bind('<Button-1>', callback)
    mywin.surf.pack()

    mywin.win.mainloop()

    p1 = []
    for p in g_p1:
        p[0] -= dh1
        p1.append(p)
    p2 = []
    for p in g_p2:
        p[0] -= dh2
        p[1] -= w1
        p2.append(p)

    return g_p1, g_p2

# V0.1 2008-12-23 10:59:13 JB
# V0.2 2008-12-27 09:35:47 JB
def image_plot_match_points(im1, im2, m1, m2, kind = 'pointlink', color = 'black'):
    '''
    Plot the two lists of points matched to PIL image data.
    => [im1]   PIL image data link with p1
    => [im2]   PIL image data link with p2
    => [m1]    list of points matched with [m2] from [im1],
               [[m1_x0, m1_y0], [m1_x1, m1_y1], ..., [m1_xi, m1_yi]]
    => [m2]    list of points matched with [m1] from [im2],
               [[m2_x0, m2_y0], [m2_x1, m2_y1], ..., [m2_xi, m2_yi]]
    => <kind>  kind of plot:
               'point'     plot list of points [m1] and [m2] on [im1] with points
               'link'      plot list of points [m1] and [m2] on [im1] with lines
               'pointlink' plot list of points [m1] and [m2] on [im1+im2] with points and lines
               (default 'pointlink')
    => <color> link color: 'black', 'red', 'green', 'white' or 'blue'
               (default black)
    <= im      PIL image data with points plotted
    '''
    import ImageDraw, sys
  
    if kind == 'point':
        draw = ImageDraw.Draw(im1)
        rad = 2
        for n in xrange(len(m1)):
            draw.ellipse((m1[n, 1] - rad, m1[n, 0] - rad, m1[n, 1] + rad, m1[n, 0] + rad), fill=(0, 255, 0))
            draw.ellipse((m2[n, 1] - rad, m2[n, 0] - rad, m2[n, 1] + rad, m2[n, 0] + rad), fill=(255, 0, 0))
    elif kind == 'link':
        draw = ImageDraw.Draw(im1)
        rad = 2
        for n in xrange(len(m1)):
            draw.line([int(m1[n, 1]), int(m1[n, 0]), int(m2[n, 1]), int(m2[n, 0])], fill=(0, 0, 0))
    elif kind == 'pointlink':
        import Image
        #surf = Image.blend(im1, im2, 0.5)
        draw = ImageDraw.Draw(im1)
        if   color == 'black': col = (0,     0,   0)
        elif color == 'white': col = (255, 255, 255)
        elif color == 'red':   col = (255,   0,   0)
        elif color == 'blue':  col = (0,     0, 255)
        elif color == 'green': col = (0,   255,   0)
        else:                  col = (0,     0,   0)
        rad = 2
        for n in xrange(len(m1)):
            draw.line([int(m1[n, 1]), int(m1[n, 0]), int(m2[n, 1]), int(m2[n, 0])], fill = col)
            draw.ellipse((m1[n, 1] - rad, m1[n, 0] - rad, m1[n, 1] + rad, m1[n, 0] + rad), fill=(0, 255, 0))
            draw.ellipse((m2[n, 1] - rad, m2[n, 0] - rad, m2[n, 1] + rad, m2[n, 0] + rad), fill=(255, 0, 0))
            
    else:
        print 'Image plot, kind of plot unknows.'
        sys.exit()

    del draw

    return im1

# V0.1 2008-12-21 00:10:17 JB
# V0.2 2009-03-27 15:51:50 JB
# v0.3 2009-08-25 10:53:03 JB
def image_plot_points(im, pts, kind = 'point', color = 'red', num = 0, rad = 3):
    '''
    Plot list of points to PIL image.
    => [im]    PIL image data
    => [pts]   list of points [[y0, x0], [y1, x1], ..., [yi, xi]]
    => <kind>  kind of plot, 'target': circles and one pixel centered to the points,
               'point': circles centered to the points,
               'pixel': only pixels set to point position
               (default 'point')
    => <color> color plot ('red', 'blue' or 'green') (default 'red')
    => <num>   set to one to diplay the point number near to the point (default set to 0)
    <= im      PIL image data with points plotted
    '''
    import ImageDraw, sys

    if   color == 'red':   col = (255, 0, 0)
    elif color == 'blue':  col = (0, 0, 255)
    elif color == 'green': col = (0, 255, 0)
    else:
        print 'Image plot point, color unknows.'
        sys.exit()

    draw = ImageDraw.Draw(im)
    if kind == 'target':
        for n in xrange(len(pts)):
            x    = pts[n][1] - 1
            y    = pts[n][0] - 1
            x, y = int(x), int(y)
            draw.point((x, y), fill=col)
            draw.ellipse((x - rad, y - rad, x + rad, y + rad), outline=col)
            if num: draw.text((x + rad, y + rad), str(n), fill=col)
    elif kind == 'point':
        for n in xrange(len(pts)):
            x    = pts[n][1] - 1
            y    = pts[n][0] - 1
            x, y = int(x), int(y)
            draw.ellipse((x - rad, y - rad, x + rad, y + rad), fill=col)
            if num: draw.text((x + rad, y + rad), str(n), fill=col)
    elif kind == 'pixel':
        for n in xrange(len(pts)):
            x    = pts[n][1] - 1
            y    = pts[n][0] - 1
            x, y = int(x), int(y)
            draw.point((x, y), fill=col)
            if num: draw.text((x, y), str(n), fill=col)
    elif kind == 'win':
        for n in xrange(len(pts)):
            x    = pts[n][1] - 1
            y    = pts[n][0] - 1
            x, y = int(x), int(y)
            draw.point((x, y), fill=col)
            draw.rectangle((x - rad, y - rad, x + rad, y + rad), outline=col)
            if num: draw.text((x, y), str(n), fill=col)
    else:
        print 'Image plot, kind of plot unknows.'
        sys.exit()

    del draw

    return im

# V0.1 2009-03-06 16:39:53 JB
def image_plot_lines(im, l1, l2, color = 'black'):
    '''
    Plot the lines according list of points to PIL image data.
    => [im]    PIL image
    => [l1]    list of points (head of the lines),
               [[l1_y0, l1_x0], [l1_y1, l1_x1], ..., [l1_yi, l1_xi]]
    => [l2]    list of points (tail of the lines),
               [[l2_y0, l2_x0], [l2_y1, l2_x1], ..., [l2_yi, l2_xi]]
    => <color> link color: 'black', 'red', 'green', 'white' or 'blue'
               (default black)
    <= im      PIL image data with lines plotted
    '''
    import ImageDraw

    draw = ImageDraw.Draw(im)
    if   color == 'black': col = (0,     0,   0)
    elif color == 'white': col = (255, 255, 255)
    elif color == 'red':   col = (255,   0,   0)
    elif color == 'blue':  col = (0,     0, 255)
    elif color == 'green': col = (0,   255,   0)
    else:                  col = (0,     0,   0)

    for n in xrange(len(l1)):
        l1x = int(l1[n][1]) + 3 # border
        l1y = int(l1[n][0]) + 3
        l2x = int(l2[n][1]) + 3
        l2y = int(l2[n][0]) + 3
        draw.line([l1x, l1y, l2x, l2y], fill = col)

    del draw

    return im

# V0.1 2008-12-20 20:13:39 JB
# V0.2 2009-03-04 15:48:11 JB
def image_im2mat(im):
    '''
    Transform PIL image to Numpy array (gray, RGB , and RGBA images)
    => [im] PIL image data
    <= mat  Numpy array, [l], [r, g, b] or [r, g, b, a]
    '''
    from numpy import array, reshape
   
    w, h = im.size
    mode = im.mode
    if mode not in ['L', 'RGB', 'RGBA']:
        print 'Mode not valide must be L, RGB, or RGBA, not %s' % mode
        sys.exit()

    if mode == 'L':
        data = im.getdata()
        tmp  = array(data)
        im   = reshape(tmp, (h, w))
        im  = im / 255.0
        return [im]
    else:
        if   mode == 'RGB':  r, g, b    = im.split()
        elif mode == 'RGBA': r, g, b, a = im.split()
        data_r    = r.getdata()
        data_g    = g.getdata()
        data_b    = b.getdata()
        tmpr      = array(data_r)
        tmpg      = array(data_g)
        tmpb      = array(data_b)
        data_r    = reshape(tmpr, (h, w))
        data_g    = reshape(tmpg, (h, w))
        data_b    = reshape(tmpb, (h, w))
        data_r    = data_r / 255.0
        data_g    = data_g / 255.0
        data_b    = data_b / 255.0
        if   mode == 'RGB':
            return [data_r, data_g, data_b]
        elif mode == 'RGBA':
            data_a  = a.getdata()
            tmpa    = array(data_a)
            data_a  = reshape(tmpa, (h, w))
            data_a  = data_a / 255.0
            return [data_r, data_g, data_b, data_a]

# V0.1 2008-12-20 20:16:51 JB
# V0.2 2009-03-05 14:11:20 JB
def image_mat2im(mat):
    '''
    Transform Numpy array to PIL image (gray, RGB, and RGBA images)
    => [mat] Numpy array [l], [r, g, b], or [r, g, b, a]
    <= im    PIL image data
    '''
    from   numpy import reshape
    from   sys   import exit
    import Image
    
    mode = len(mat)
    if mode not in [1, 3, 4]:
        print 'Mode not valide must be L, RGB, or RGBA, not %s' % mode
        exit()
    
    w    = len(mat[0][0])
    h    = len(mat[0])
    nbp  = w * h
    if mode == 1:
        mat  = mat[0] * 255
        mat  = list(reshape(mat, (nbp)))
        im   = Image.new('L', (w, h), 255)
        im.putdata(mat)
        return im
    else:
        r   = mat[0] * 255
        g   = mat[1] * 255
        b   = mat[2] * 255
        r   = list(reshape(r, (nbp)))
        g   = list(reshape(g, (nbp)))
        b   = list(reshape(b, (nbp)))
        imr = Image.new('L', (w, h), 255)
        img = Image.new('L', (w, h), 255)
        imb = Image.new('L', (w, h), 255)
        imr.putdata(r)
        img.putdata(g)
        imb.putdata(b)
        if mode == 3:
            im  = Image.merge('RGB', (imb, img, imb))
            return im
        elif mode == 4:
            a   = mat[3] * 255
            a   = list(reshape(mat[3], (nbp)))
            ima = Image.new('L', (w, h), 255)
            ima.putdata(a)
            im  = Image.merge('RGBA', (imb, img, imb, ima))
            return im

# V0.1 2008-12-07 00:35:17 JB
def image_anaglyph(imr, iml):
    '''
    Create anaglyph image (3D) from right and left images, return image
    => [imr] right PIL image data
    => [iml] left PIL image data
    <= anaglyphe PIL image data
    '''
    import Image

    # split
    rr, gr, br = imr.split()
    rl, gl, bl = iml.split()

    # process
    new_gr  = Image.new('L', gr.size, 255)
    new_rl  = Image.new('L', rl.size, 255)
    new_bl  = Image.new('L', bl.size, 255)
    new_imr = Image.merge('RGB', (br, new_gr, rr))
    new_iml = Image.merge('RGB', (new_bl, gl, new_rl))
    im_anag = Image.blend(new_imr, new_iml, 0.5)
 
    return im_anag

## COLOR ####################
# V0.1 2008-12-20 15:24:37 JB
def color_color2gray(im):
    '''
    Convert color image to gray image
    => [im] color PIL image data
    <= im gray PIL image data
    '''
    return im.convert('L')

# V0.1 2009-03-27 15:41:14 JB
def color_gray2color(im):
    '''
    Convert gray image to color image
    => [im] color PIL image data
    <= im gray PIL image data
    '''
    return im.convert('RGB')

# V0.1 2008-12-20 21:11:38 JB
def color_norm_gray(mat):
    '''
    Normalize gray scale color of a numpy array (0 to 255)
    => [mat] Numpy array L or RGB
    <= mat   Numpy array normalized
    '''
    norm = []
    for c in xrange(len(mat)):
        vmin, vmax = mat[c].min(), mat[c].max()
        s    = 1.0 / abs(vmin - vmax)
        tmp  = (mat[c] - vmin) * s
        norm.append(tmp)

    return norm

## SPACE ####################

# V0.1 2008-12-20 20:50:11 JB
def space_gauss(w, sig):
    '''
    Create the 2D Gaussienne matrix (numpy array)
    => [w]   window size, must be odd
    => [sig] sigma value to the Gauss function
    <= mat   Numpy array
    '''
    from numpy import zeros
    from math  import exp
    import sys

    # check
    if w % 2 !=1:
        print 'Gaussienne matrix must be odd.'
        sys.exit()

    sig  = float(sig)
    mat  = zeros((w, w))
    ct_i = 0
    for i in xrange(-(w // 2), w // 2 + 1, 1):
        ct_j = 0
        for j in xrange(-(w // 2), w // 2 + 1, 1):
            mat[ct_i, ct_j] = exp(-(i*i + j*j) / (2 * sig * sig))
            ct_j += 1
        ct_i += 1

    return mat

# V0.1 2009-08-21 05:59:24 JB
def space_mask_blending(h, w, a, b, c = 1.0):
    '''
    Mask blending
    => [h] size image
    => [w] size image
    => [a] alpha
    => [b] beta
    => [c] gamma
    <= mask numpy array only luminance
    More details see Bert 2007 thesis p121
    '''
    from numpy import zeros
    maskw = zeros((h, w))
    aw    = int(a * w) // 2
    bw    = int(b * w) // 2
    cw    = int(c * w) // 2
    vw    = []
    for x in xrange(aw, bw):
        vw.append(x / float(bw - aw) + aw / float(aw - bw))
    for x in xrange(bw, cw):
        vw.append(1.0)

    for line in xrange(h):
        maskw[line, aw:cw] = vw
    aw = w - aw
    cw = w - cw
    vw.sort(reverse = True)
    for line in xrange(h):
        maskw[line, cw:aw] = vw

    maskh = zeros((h, w))
    ah    = int(a * h) // 2
    bh    = int(b * h) // 2
    ch    = int(c * h) // 2
    vh    = []
    for y in xrange(ah, bh):
        vh.append(y / float(bh - ah) + ah / float(ah - bh))
    for y in xrange(bh, ch):
        vh.append(1.0)

    for col in xrange(w):
        maskh[ah:ch, col] = vh
    ah = h - ah
    ch = h - ch
    vh.sort(reverse = True)
    for col in xrange(w):
        maskh[ch:ah, col] = vh

    # fix bug if image is odd
    if w % 2 == 1:
        cw = (w - 1) // 2
        for y in xrange(h): maskw[y, cw] = 1.0
    if h % 2 == 1:
        ch = (h - 1) // 2
        for x in xrange(w): maskh[ch, x] = 1.0

    mask = maskw * maskh

    return mask

# V0.1 2008-12-20 20:07:41 JB
def space_conv(matim, mat):
    '''
    Space convolution between two matrices (numpy format)
    => [matim] Numpy array as image
    => [mat]   Numpy array as convolution matrix
    <= res     Numpy array, result of the convolution (same size as [matim])
    '''
    from numpy import zeros
    import sys

    # check
    if len(mat[0]) != len(mat):
        print 'Convolution matrix must be square.'
        sys.exit()
        
    if len(mat) % 2 != 1:
        print 'Convolution matrix must be odd.'
        sys.exit()
    
    h, w = len(matim), len(matim[0])
    res  = zeros((h, w))
    dmat = len(mat) // 2
    for i in xrange(dmat, h - dmat):
        for j in xrange(dmat, w - dmat):
            res[i, j] = sum(sum(mat * matim[i-dmat:i+dmat+1, j-dmat:j+dmat+1])) 
    
    return res

# V0.1 2008-12-20 15:40:43 JB
# V0.2 2008-12-20 20:33:05 JB
def space_conv_im(im, mat):
    '''
    Space convolution between image and a matrix
    => [im]  PIL image data
    => [mat] Numpy array as convolution matrix
    <= res   PIL image data, result of the convolution (same size as [im])

    '''
    from numpy import array
    import sys

    # check
    if im.mode != 'L':
        print 'Image must be in gray color.'
        sys.exit()

    if len(mat[0]) != len(mat):
        print 'Convolution matrix must be square.'
        sys.exit()
        
    if len(mat) % 2 != 1:
        print 'Convolution matrix must be odd.'
        sys.exit()
    
    # convolution
    matim = image_im2mat(im)
    mat   = array(mat)
    res   = space_conv(matim, mat)
    im    = image_mat2im(res)

    return im

# V0.1 2008-12-20 23:36:14 JB
def space_non_max_supp(mat, sw):
    '''
    Extract local maximum value to Numpy matrix
    => [mat] input Numpy array
    => [sw]  size of window local research (must be odd)
    <= res   Numpy array with local maximum value
    '''
    from numpy import zeros

    h, w = len(mat), len(mat[0])
    res  = zeros((h, w))
    rad  = sw // 2
    for i in xrange(rad, h - rad):
        for j in xrange(rad, w - rad):
            vmax = mat[i-rad:i+rad+1, j-rad:j+rad+1].max()
            if  vmax == mat[i, j]: res[i, j] = mat[i, j] 

    return res

# V0.1 2008-12-21 10:20:16 JB
def space_harris_ctl(mat, nb_pts):
    '''
    Control threshold loop to harris matrix, this function return
    the corner feature according the number of points desired.
    => [mat]    Numpy array given by Harris detector
    => [nb_pts] number of points desired
    <= pts      list of features selected [[y0, x0], [y1, x1], ..., [yi, xi]]
    '''
    for th in xrange(256):        
        pts = space_harris_th(mat, th)
        if len(pts) <= nb_pts: return pts

    return space_harris_th(mat, 0)

# V0.1 2008-12-20 23:57:37 JB
def space_harris_th(mat, th):
    '''
    Extract corner feature according the value matrix
    given by Harris detector and a threshold
    => [mat] Numpy array given by Harris detector
    => [th]  threshold value used to extract features
    <= pts   list of features selected [[y0, x0], [y1, x1], ..., [yi, xi]]
    '''
    from numpy import nonzero, array, zeros

    ind = nonzero(mat >= th)
    nbp = len(ind[0])
    if nbp == 0: return array([[], []])
    pts = zeros((nbp, 2))
    for n in xrange(nbp):
        pts[n, 0] = ind[0][n]
        pts[n, 1] = ind[1][n]

    return pts
    
# V0.1 2008-12-20 20:33:30 JB
def space_harris(im):
    '''
    Harris detector
    => [im] PIL image data
    <= res  Numpy array, response of the corner detector
    '''
    from numpy import array

    dx  = [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]
    dx  = array(dx)
    dy  = dx.transpose()
    im  = color_color2gray(im)
    mat = image_im2mat(im)
    print mat
    Ix  = space_conv(mat, dx)
    Iy  = space_conv(mat, dy)
    G   = space_gauss(13, 2)
    Ix2 = space_conv(Ix * Ix, G)
    Iy2 = space_conv(Iy * Iy, G)
    Ixy = space_conv(Ix * Iy, G)
    M   = (Ix2 * Iy2 - Ixy * Ixy) - 0.04 * (Ix2 + Iy2) ** 2 
    M   = color_norm_gray(M)
    
    return space_non_max_supp(M, 7)

# V0.1 2009-03-09 11:42:34 JB
# V0.2 2009-08-17 10:26:06 JB
def space_reg_ave(lmat, p, ws, tx, ty, N = -1):
    '''
    Images average after registration by grid alignment
    => [lmat] list of images (numarray [L] or [R, G, B])
    => [p]    feature point tracked [y, x]
    => [ws]   window size tracked (must be odd)
    => [tx]   delta x to align (from p-tx to p+tx)
    => [ty]   delta y to align (from p-ty to p+ty)
    => <N>    number of images used in lmat list (default -1 meaning all)
    <= ave    result average (numarry only luminance)
    '''
    from numpy import zeros, ones
    xt, yt  = 0, 0
    dummy   = lmat[0]
    mode    = len(dummy)
    h, w    = dummy[0].shape
    if N == -1: nb_mat  = len(lmat)
    else:       nb_mat  = N
    ave_mat = lmat[0]
    mask    = ones((h, w))
    for n in xrange(nb_mat - 1):
        if mode == 1:
            mat1 = lmat[n][0].copy()
            mat2 = lmat[n + 1][0].copy()
        elif mode == 3:
            im1  = image_mat2im(lmat[n])
            im2  = image_mat2im(lmat[n + 1])
            im1  = color_color2gray(im1)
            im2  = color_color2gray(im2)
            mat1 = image_im2mat(im1)[0]
            mat2 = image_im2mat(im2)[0]

        xp, yp   = space_align(mat1, mat2, p, ws, tx, ty)

        p[0] += yp
        p[1] += xp
        xt   += xp
        yt   += yp
        print 'im:', n, n + 1, 'dx:', xp, 'dy:', yp

        for j in xrange(h):
            for i in xrange(w):
                xm = i - xt
                ym = j - yt
                if xm > 0 and xm < w and ym > 0 and ym < h:
                    for c in xrange(mode):
                        ave_mat[c][ym, xm] = ave_mat[c][ym, xm] + lmat[n + 1][c][j, i]
                    mask[ym, xm]    += 1

    for c in xrange(mode): ave_mat[c] = ave_mat[c] / float(nb_mat)
 
    j = 0
    while j < h:
        ct_w = 0
        i    = 0
        while i < w:
             if int(mask[j, i]) == nb_mat:
                 ct_w += 1
             i += 1
        if ct_w != 0:
            break
        j += 1

    i = 0
    while i < w:
        ct_h = 0
        j    = 0
        while j < h:
            if mask[j, i] == nb_mat:
                ct_h += 1
            j += 1
        if ct_h != 0: break
        i += 1

    print ct_w, ct_h
 
    if   mode == 1: crop = [zeros((ct_h, ct_w))]
    elif mode == 3: crop = [zeros((ct_h, ct_w)), zeros((ct_h, ct_w)), zeros((ct_h, ct_w))]
    ct_i, ct_j = 0, 0
    for j in xrange(h):
        ct_i = 0
        for i in xrange(w):
            if mask[j, i] == nb_mat:
                for c in xrange(mode):
                    crop[c][ct_j, ct_i] = ave_mat[c][j, i]

                ct_i += 1
        if ct_i != 0: ct_j += 1
          
    crop = color_norm_gray(crop)

    return crop

# V0.1 2009-03-07 11:33:27 JB
def space_align(I1, I2, p1, sw, tx, ty, p2 = -1):
    '''
    Gridding aligment method between two images
    => [I1]   image 1 (numarray only luminance)
    => [I2]   image 2 (numarray only luminance)
    => [p1]   feature point tracked [y, x]
    => [sw]   window size tracked (must be odd)
    => [tx]   delta x to align (from p-tx to p+tx)
    => [ty]   delta y to align (from p-ty to p+ty)
    => <p2>   if the feature point tracked is known in the second image,
              in this case used to refine the alignment (see mosaicing),
              (default -1 meanning same position as p1)
    <= xp, yp relative alignment parameters
    '''

    # I1 and I2 are mat
    rad  = sw // 2
    x1   = p1[1]
    y1   = p1[0]
    w    = len(I1[0])
    h    = len(I1)
    i1   = I1[y1 - rad:y1 + rad + 1, x1 - rad:x1 + rad + 1]

    xp   = 0
    yp   = 0
    vmin = 1e9
    if p2 == -1:
        x2 = x1
        y2 = y1
    else:
        x2 = p2[1]
        y2 = p2[0]
    for y in xrange(y2 - ty, y2 + ty + 1):
        for x in xrange(x2 - tx, x2 + tx + 1):
            i2 = I2[y - rad:y + rad + 1, x - rad:x + rad + 1]
            e  = (i2 - i1)
            e  = e * e
            v  = e.sum()
            if v < vmin:
                vmin   = v
                xp, yp = x, y
            #print 'x:', x, 'y:', y, 'v:', v

    return xp - x1, yp - y1

# V0.1 2009-08-16 13:08:05 JB
def space_merge(I1, I2, p1, p2, method = 'ave'):
    '''
    Merge two images into another one according their alignment parameters
    => [I1]     image 1 (numarray [L] or [R, G, B])
    => [I2]     image 2 (numarray [L] or [R, G, B])
    => [p1]     interest point to image 1 [[y1, x1]]
    => [p2]     same interest point p1 to image 2 [[y2, x2]]
    => [method] merging mode 'ave' average or 'ada' adaptative
    <= I3       result image L or RGB
    '''
    from numpy import zeros
    I1     = color_norm_gray(I1)
    I2     = color_norm_gray(I2)
    mode   = len(I1)
    y1, x1 = p1[0][0], p1[0][1]
    y2, x2 = p2[0][0], p2[0][1]
    h1, w1 = I1[0].shape
    h2, w2 = I2[0].shape
    # changing ref
    l1, t1 = -x1, -y1
    l2, t2 = -x2, -y2
    r1, b1 = w1 - x1 - 1, h1 - y1 - 1
    r2, b2 = w2 - x2 - 1, h2 - y2 - 1
    # size res image
    lr = min(l1, l2)
    tr = min(t1, t2)
    rr = max(r1, r2)
    br = max(b1, b2)
    hr = br - tr + 1
    wr = rr - lr + 1
    if   mode == 1: res = [zeros((hr, wr))]
    elif mode == 3: res = [zeros((hr, wr)), zeros((hr, wr)), zeros((hr, wr))]
    # paste first images
    for c in xrange(mode):
        for h in xrange(h1):
            href = h - y1
            hglo = href - tr
            for w in xrange(w1):
                wref = w - x1
                wglo = wref - lr
                #res[c][hglo, wglo] = (res[c][hglo, wglo] + I1[c][h, w]) / 2.0
                res[c][hglo, wglo] = I1[c][h, w]

    # paste the second one
    for c in xrange(mode):
        for h in xrange(h2):
            href = h - y2
            hglo = href - tr
            for w in xrange(w2):
                wref = w - x2
                wglo = wref - lr
                #res[c][hglo, wglo] = (res[c][hglo, wglo] + I2[c][h, w]) / 2.0
                res[c][hglo, wglo] = I2[c][h, w]

    if method == 'ave': return res

    mask1  = space_mask_blending(h1, w1, 0, 0.2)
    # in ref
    lo  = max(l1, l2)
    to  = max(t1, t2)
    ro  = min(r1, r2)
    bo  = min(b1, b2)
    # in image
    lo1 = lo + x1
    to1 = to + y1
    lo2 = lo + x2
    to2 = to + y2
    # in global
    log = lo - lr
    rog = ro - lr
    tog = to - tr
    bog = bo - tr
    
    wo  = rog - log + 1
    ho  = bog - tog + 1

    for c in xrange(mode):
        jog = tog
        jo1 = to1
        jo2 = to2
        for h in xrange(ho):
            iog = log
            io1 = lo1
            io2 = lo2
            for w in xrange(wo):
                res[c][jog, iog] = (1 - mask1[jo1, io1]) * I2[c][jo2, io2] + mask1[jo1, io1] * I1[c][jo1, io1]
                #res[c][tog, iog] = mask1[to1, io1] #* I1[c][to1, io1]
                #res[c][tog, iog] = (1 - mask1[to1, io1]) #* I2[c][to2, io2]
                #res[c][jog, iog] = 1.0
                
                iog += 1
                io1 += 1
                io2 += 1

            jog += 1
            jo1 += 1
            jo2 += 1

    return res

# V0.1 2009-03-06 14:13:46 JB
def lucas_kanade(im1, im2, p, sw, maxit):
    '''
    Lucas-Kanade
    !!! DRAFT !!!
    '''
    from numpy import array, matrix
    from Image import BICUBIC
    from sys   import exit
    rad  = sw // 2
    dx   = [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]
    dx   = array(dx)
    dy   = dx.transpose()
    im1  = color_color2gray(im1)
    im2  = color_color2gray(im2)
    w, h = im2.size
    mat1 = image_im2mat(im1)
    I1   = array(mat1[0])
    I1   = I1 / 255.0
    i1   = I1[p[0][0]-rad:p[0][0]+rad+1, p[0][1]-rad:p[0][1]+rad+1]
    
    #buf = image_mat2im([i1])
    #image_show(buf)

    Ix   = space_conv(I1, dx)
    print 'Ix [ok]'

    Iy   = space_conv(I1, dy)
    print 'Iy [ok]'

    ix   = Ix[p[0][0]-rad:p[0][0]+rad+1, p[0][1]-rad:p[0][1]+rad+1]
    iy   = Iy[p[0][0]-rad:p[0][0]+rad+1, p[0][1]-rad:p[0][1]+rad+1]

    #buf = image_mat2im([ix])
    #image_show(buf)

    #buf = image_mat2im([iy])
    #image_show(buf)

    G    = space_gauss(13, 2)

    Ix2  = space_conv(Ix * Ix, G)
    
    #Ix2  = Ix * Ix
    #Ix2  = color_norm_gray(Ix2)
    print 'Ix2 [ok]'
    
    Iy2  = space_conv(Iy * Iy, G)
    
    #Iy2  = Iy * Iy
    #Iy2  = color_norm_gray(Iy2)
    print 'Iy2 [ok]'
    Ixy  = space_conv(Ix * Iy, G)
    #Ixy  = Ix * Iy
    #Ixy  = color_norm_gray(Ixy)
    print 'Ixy [ok]'
    ix2  = Ix2[p[0][0]-rad:p[0][0]+rad+1, p[0][1]-rad:p[0][1]+rad+1]
    iy2  = Iy2[p[0][0]-rad:p[0][0]+rad+1, p[0][1]-rad:p[0][1]+rad+1]
    ixy  = Ixy[p[0][0]-rad:p[0][0]+rad+1, p[0][1]-rad:p[0][1]+rad+1]

    # print ix2

    #buf = image_mat2im([ix2])
    #image_show(buf)

    #buf = image_mat2im([iy2])
    #image_show(buf)

    #buf = image_mat2im([ixy])
    #image_show(buf)


    F    = matrix([[ix2.sum(), ixy.sum()], [iy2.sum(), ixy.sum()]])
    V    = array([[0], [0]])
    u, v = 0, 0
    for it in xrange(maxit):
        out = im2.resize((w - u, h - v), BICUBIC)
        #print out.size
        mat2 = image_im2mat(out)
        I2   = array(mat2[0])
        I2   = I2 / 255.0
        i2   = I2[p[0][0]-rad:p[0][0]+rad+1, p[0][1]-rad:p[0][1]+rad+1]
        it   = i2 - i1
        ixt  = ix * it
        iyt  = iy * it
        T    = matrix([[ixt.sum()], [iyt.sum()]])
        #print F
        #print T
        #print V
        V    = F.I * T
        V    = V.getA()
        u    = u - (V[0] * 20.0)
        v    = v - (V[1] * 20.0)
        #print 'eu', V[0], 'ev', V[1], 'u', u[0], 'v', v[0]
        print u[0], v[0]

# V0.1 2008-12-23 09:28:25 JB
# V0.2 2008-12-24 08:43:38 JB
def space_match_points(im1, im2, p1, p2, sw, kind='full'):
    '''
    Match list of points p1 with list of points p2 according
    texture distance of windows centered to each point. All points are
    search and distance is define as Squared Euclidean.
    => [im1]  PIL image data as image 1
    => [im2]  PIL image data as image 2
    => [p1]   list of points p1 from [mat1], [[y0, x0], ..., [yi, xi]]
    => [p2]   list of points p2 from [mat2], [[y0, x0], ..., [yi, xi]]
    => [sw]   size of window in order to calculate the distance, must be odd (window centered to point)
    => [kind] kind of window, 'full' or 'cha' (default 'full')
    <= m1     list of points m1 order with match list of points m2
    <= m2     list of points m2 order with match list of points m1
    m1 = [[m1_y0, m1_x0], [m1_y1, m1_x1], ..., [m1_xi, m1_yi]]
                |               |                    |
    m2 = [[m2_y0, m2_x0], [m2_y1, m2_x1], ..., [m2_xi, m2_yi]]
    '''
    from numpy import zeros
    import sys

    im1  = color_color2gray(im1)
    im2  = color_color2gray(im2)
    mat1 = image_im2mat(im1)
    mat2 = image_im2mat(im2)

    if len(mat1) != len(mat2) or len(mat1[0]) != len(mat2[0]):
        print 'Images must be the same sizes.'
        sys.exit()

    # check points out of works area due to size of window
    rad  = sw // 2
    pts1 = []
    for p in p1:
        if p[0]-rad < 0 or p[0]+rad >= len(mat1) or p[1]-rad < 0 or p[1]+rad+1 >= len(mat1[0]):
            continue
        else: pts1.append(p)

    pts2 = []
    for p in p2:
        if p[0]-rad < 0 or p[0]+rad >= len(mat2) or p[1]-rad < 0 or p[1]+rad+1 >= len(mat2[0]):
            continue
        else: pts2.append(p)

    if len(pts2) < 1:
        print 'Not enough points p2.'
        sys.exit()

    # matching
    nb = min(len(pts1), len(pts2))
    m1, m2 = zeros((nb, 2)), zeros((nb, 2))
    for j in xrange(len(pts1)):
        if kind == 'cha':
            sub1 = mat1[pts1[j][0]-rad:pts1[j][0]+rad+1:2, pts1[j][1]-rad:pts1[j][1]+rad+1:2]
        else:
            sub1 = mat1[pts1[j][0]-rad:pts1[j][0]+rad+1, pts1[j][1]-rad:pts1[j][1]+rad+1]
        best = -1
        dmin = 1e10

        if len(pts2) == 0: break
        for i in xrange(len(pts2)):
            if kind == 'cha':
                sub2 = mat2[pts2[i][0]-rad:pts2[i][0]+rad+1:2, pts2[i][1]-rad:pts2[i][1]+rad+1:2]
            else:
                sub2 = mat2[pts2[i][0]-rad:pts2[i][0]+rad+1, pts2[i][1]-rad:pts2[i][1]+rad+1]
            dist = sum(sum((sub1 - sub2)**2))
            if dist < dmin:
                dmin = dist
                best = i

        m1[j, 0] = pts1[j][0]
        m1[j, 1] = pts1[j][1]
        m2[j, 0] = pts2[best][0]
        m2[j, 1] = pts2[best][1]
        pts2.pop(best)
    
    return m1, m2

# V0.1 2009-08-28 03:42:33 JB
def space_G_transform(G, im, method = 0):
    '''
    Apply homography transformation to an PIL image
    => G        homography matrix (numpy array 3x3)
    => im       PIL image (L or RGB)
    => <method> method use to warp image 'NEAREST', 'BILINEAR' or 'BICUBIC'
    <= res      PIL image transformed
    '''
    from numpy import matrix, zeros
    from sys   import stdout

    GI   = G.I
    w, h = im[0].size
    c0   = G * matrix([0, 0, 1]).T
    c1   = G * matrix([w, 0, 1]).T
    c2   = G * matrix([w, h, 1]).T
    c3   = G * matrix([0, h, 1]).T

    l = min(c0[0], c1[0], c2[0], c3[0])
    r = max(c0[0], c1[0], c2[0], c3[0])
    t = min(c0[1], c1[1], c2[1], c3[1])
    b = max(c0[1], c1[1], c2[1], c3[1]) 
    l = int(l)
    r = int(r)
    t = int(t)
    b = int(b)

    wim  = r - l + 1
    him  = b - t + 1
    mat1 = image_im2mat(im)
    Ch   = len(mat1)
    mat2 = []
    for c in xrange(Ch): mat2.append(zeros((him, wim)))
    
    pixy = 0
    for y in xrange(t, b + 1):
        pixx = 0
        for x in xrange(l, r + 1):
            p1t        = GI * matrix([x, y, 1]).T
            p1t       /= p1t[2]
            p1t        = p1t.astype('int32')
            p1t        = p1t.T
            x1, y1, z1 = p1t.tolist()[0]
            x1i, y1i   = int(x1), int(y1)
            if x1i < 0 or x1i >= w or y1i < 0 or y1i >= h: continue

            if   method == 'NEAREST':
                for c in xrange(Ch):
                    mat2[c][pixy, pixx] = mat1[c][y1i, x1i]
            elif method == 'BILINEAR':
                a0  = x1 - x1i
                a1  = 1 - a0
                a2  = y1 - y1i
                a3  = 1 - a2
                A   = array([[0, a2, 0], [a1, 1.0, a0], [0, a3, 0]])
                # here need to check not over < 0 or > w, h
                for c in xrange(Ch):
                    pix = mat1[c][y1i-1:y1i+2, x1i-1:x1i+2]
                    pix = pix * A
                    pix = pix.sum() / 5.0
                    mat2[c][pixy, pixx] = pix
                

            pixx += 1

        pixy += 1
        stdout.write('\rprocess %6.2f' % (pixy / float(him)) * 100)
 
    print ''

    return mat2

## GEOMETRY ######################

# V0.1 2009-08-27 07:45:51 JB
def geo_homography(p1, p2):
    '''
    Compute the homography matrix (need at least 4 points per pair)
    use DLT method (Direct Linear Transformation)
    => [p1] list of points p1 [[y0, x0], ..., [yi, xi]]
    => [p2] list of points matched with p1 [[y0, x0], ..., [yi, xi]]
    <= [H]  Homogenous homography array [3x3] 
    '''
    from numpy import zeros, linalg, reshape, matrix

    p1, T1 = stats_norm2D_pts(p1)
    p2, T2 = stats_norm2D_pts(p2)
    A = zeros((2 * len(p1), 9))
    for n in xrange(len(p1)):
        y1, x1       = p1[n]
        y2, x2       = p2[n]
        A[2 * n]     = [ 0,  0, 0, -x1, -y1, -1,  y2*x1,  y2*y1,  y2] 
        A[2 * n + 1] = [x1, y1, 1,   0,   0,  0, -x2*x1, -x2*y1, -x2]

    U, S, V  = linalg.svd(A)
    G        = V[8].reshape((3, 3))
    G       /= G[2, 2]
    G        = T2.I * G * T1

    return matrix(G)

## STATISTICS ####################

# V0.1 2009-09-01 17:58:15 JB
def stats_norm2D_pts(p):
    '''
    Normalize point in order the average distance between points and
    centroid is equal to sqrt(2). This is used to compute the 
    homography according Hartley and Zisserman normalization.
    => [p]  list of points [[y0, x0], ..., [yi, xi]]
    <= newp list of points normalize, same format as p
    <= T    transformation matrix used to normalize, numpy matrix format 3x3
    '''
    from numpy import zeros, matrix, sqrt, mean

    n = len(p)
    y = zeros((n))
    x = zeros((n))
    for i in xrange(n):
        y[i] = p[i][0]
        x[i] = p[i][1]
    cx, cy = mean(x), mean(y)
    newx   = x - cx
    newy   = y - cy
    dist   = 0
    for i in xrange(n): dist += sqrt(newy[i]*newy[i] + newx[i]*newx[i])
    dist  /= float(n)
    scale  = sqrt(2) / dist
    T      = matrix([[scale, 0, -scale * cx], [0, scale, -scale * cy], [0, 0, 1]])
    newp   = []
    for i in xrange(n):
        p = T * matrix([x[i], y[i], 1]).T
        p = p.T.tolist()[0]
        newp.append([p[1], p[0]])

    return newp, T

# V0.1 2008-12-27 11:00:59 JB
def stats_dist_pts(pts1, pts2):
    '''
    Return list of distances between list of points pts1 and pts2
    => [pts1] Numpy list [[y0, x0], ..., [yi, xi]]
    => [pts2] Numpy list [[y0, x0], ..., [yi, xi]]
    <= [d]    Numpy list of distance between pts1 and pts2 [d0, ..., di]
              Euclidean distance
    '''
    from numpy import array
    from math  import sqrt
    d = []
    for n in xrange(len(pts1)):
        d.append(sqrt((pts2[n, 0] - pts1[n, 0])**2 + (pts2[n, 1] - pts1[n, 1])**2))

    return array(d)

# V0.1 2008-12-27 11:13:57 JB
def stats_ori_pts(pts1, pts2, kind = '-pi+pi'):
    '''
    Return the orientation angle composed by the vector pts1 and pts2.
    The point pts1 is defined as base and pts2 as head.
    => [pts1]  Numpy list of base points vector [[y0, x0], ..., [yi, xi]]
    => [pts2]  Numpy list of head points vector [[y0, x0], ..., [yi, xi]]
    => <kind>  orientation angle range: '-pi+pi' or '02pi' (default '-pi+pi')
    <= [alpha] Numpy list of vector orientation in degree [a0, ..., ai]
    '''
    from math  import atan, pi, sqrt
    from numpy import array

    A = []
    for n in xrange(len(pts1)):
        dx    = pts2[n, 1] - pts1[n, 1]
        dy    = pts2[n, 0] - pts1[n, 0]
        norm  = sqrt(dy*dy + dx*dx)
        dx   /= norm
        dy   /= norm
        
        if kind == '02pi':
            if   dx  < 0:              a = atan(dy / dx) + pi
            elif dx  > 0  and dy >= 0: a = atan(dy / dx)
            elif dx  > 0  and dy <  0: a = atan(dy / dx) + 2 * pi
            elif dx == 0  and dy >  0: a = pi / 2.0
            elif dx == 0  and dy <  0: a = 3 * pi / 2.0
        else:
            if   dx  > 0:              a = atan(dy / dx)
            elif dx  < 0  and dy >= 0: a = atan(dy / dx) + pi
            elif dx  < 0  and dy <  0: a = atan(dy / dx) - pi
            elif dx == 0  and dy >  0: a = pi / 2.0
            elif dx == 0  and dy <  0: a = - pi / 2.0

        a = a * 180 / pi
        A.append(a)
    
    return array(A)

# V0.1 2008-12-28 10:01:00 JB
def stats_hist(list_val, step):
    '''
    Return histogram of the input list of values
    => [list_val] list of values
    => [step]     number of groups in the histogram
    <= [hist]     list of value of population bar graph
    <= [x]        list of value of step bar graph
    '''
    minval  = min(list_val)
    maxval  = max(list_val)
    valstep = (maxval - minval) / float(step)
    rstep   = [minval] * step
    for n in xrange(1, step): rstep[n] = rstep[n - 1] + valstep
    hist    = [0] * step
    for n in xrange(step - 1):
        for val in list_val:
            if val >= rstep[n] and val < rstep[n + 1]:
                hist[n] += 1
    
    for val in list_val:
        if val >= rstep[-1]:
            hist[-1] += 1

    for n in xrange(step): rstep[n] += (valstep / 2.0)

    return hist, rstep

# V0.1 2008-12-30 11:34:06 JB
def stats_hist_clean_ori_pts(p1, p2, step):
    hist, x = stats_hist(ang, 36)
    step = x[0]
    maxhist = max(hist)
    indhist = hist.index(maxhist)

# V0.1 2008-12-28 11:11:04 JB
# V0.2 2008-12-29 16:51:28 JB
def stats_ransac_trans(p1, p2, th, nbcons, maxit):
    '''
    RANSAC algorithm for a translation model (tx, ty)
    => [p1]     Numpy list of points match with [p2]
    => [p2]     Numpy list of points match with [p1]
    => [th]     threshold consensus fitting model (in pixel))
    => [nbcons] number of elements required in consensus set
    => [maxit]  maximum iterations, if 'auto' test all points
    <= [tx, ty] model found
    <= [err]    SSE between model and consensus set
    <= [ID]     list of ID pts in the best consensus set
    '''
    from random import randrange
    from math   import sqrt
    from copy   import deepcopy

    nb_pts      = len(p1)
    ite, mx, my = 0, 0, 0
    best_cons   = []
    min_err     = 1e10

    if isinstance(maxit, basestring):
        if maxit == 'auto':
            maxit = nb_pts
            flag  = True
    else:
        flag  = False

    while ite < maxit:
        if flag: inliers = ite 
        else:    inliers = randrange(nb_pts)
        ty = p2[inliers, 0] - p1[inliers, 0]
        tx = p2[inliers, 1] - p1[inliers, 1]
        cons_set = []
        cons_set.append(inliers)
        
        err = 0
        for n in xrange(nb_pts):
            if n == inliers: continue
            dist = sqrt((p2[n, 0] - p1[n, 0] - ty)**2 + (p2[n, 1] - p1[n, 1] - tx)**2)
            
            if dist < th:
                cons_set.append(n)
                err += dist
            
        if len(cons_set) > nbcons:
            err /= len(cons_set)
            if err < min_err:
                mx, my    = tx, ty
                min_err   = err
                best_cons = deepcopy(cons_set)

        ite += 1

    return [mx, my], min_err, best_cons
    
# V0.1 2008-12-28 12:55:37 JB
def stats_list_stat(val):
    '''
    Return some stats value from a list of values
    => [val] list of value (1d)
    <= [min] value min
    <= [max] value max
    <= [ave] average value
    <= [std] standard deviation value
    '''
    from math import sqrt
    
    valmin = min(val)
    valmax = max(val)
    ave    = sum(val) / float(len(val))
    std    = 0
    for v in val: std += (v - ave)**2
    std   /= len(val)
    std    = sqrt(std)

    return valmin, valmax, ave, std

# V0.1 2008-12-29 17:04:30 JB
def stats_LMS_trans(p1, p2):
    '''
    LMS algorithm for a translation model (tx, ty)
    => [p1]     Numpy list of points match with [p2]
    => [p2]     Numpy list of points match with [p1]
    <= [tx, ty] model found
    <= [err]    SSE between model and consensus set
    <= [ID]     list of ID pts in the best consensus set
    '''
    import sys

    N  = len(p1)
    mx = []
    for n in xrange(N):
        print n, p2[n, 1] - p1[n, 1]
        mx.append(p2[n, 1] - p1[n, 1])

    sys.exit()
    N      = len(p1)
    dx, dy = [], []
    for n in xrange(N):
        dx.append(p2[n, 1] - p1[n, 1])
        dy.append(p2[n, 0] - p1[n, 0])

    Erx, Ery = [], []
    xx, yy   = [], []
    ct       = 0
    for i in xrange(N - 1):
        for j in xrange(i + 1, N):
            ex = dx[i] - dx[j]
            ey = dy[i] - dy[j]
            Erx.append([ex, ct])
            Ery.append([ey, ct])
            xx.append(ex)
            yy.append(ey)
            ct += 1

    Erx.sort()
    Ery.sort()
    exmin, exmax, exmean, exstd = stats_list_stat(xx)
    eymin, eymax, eymean, eystd = stats_list_stat(yy)

    thx  = exstd / 2.0
    memx = []
    pr1  = []
    pr2  = []
    ct   = 0
    for i in xrange(N - 1):
        for j in xrange(i + 1, N):
            if Erx[ct][0] > -thx and Erx[ct][0] < thx:
                if i not in memx:
                    print Erx[ct][0]
                    memx.append(i)
                    pr1.append(p1[i])
                    pr2.append(p2[i])
            ct += 1

    return pr1, pr2
    
## RESTORATION #############################

# V0.1 2009-08-15 04:26:02 JB
def resto_wiener(mat):
    '''
    Wiener filter from scipy
    => [mat]    Numpy array
    <= wmat     Numpy array after restoration by Wiener filter
    '''
    from scipy.signal import wiener
    #im  = image_im2mat(im)
    res = wiener(mat)
    #res = image_mat2im(res)

    return res
    
