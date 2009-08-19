#!/usr/bin/env python

## Convention
# import
# constants
# shell functions
# cmd functions
# shell io
# parser and caller

#=== import =====================

from   pymir_kernel import image_read, image_write
from   pymir_kernel import image_im2mat, image_mat2im
from   pymir_kernel import image_show, image_show_grid, image_show_get_pts
from   pymir_kernel import image_plot_points, image_plot_lines
from   pymir_kernel import color_color2gray, color_gray2color
from   pymir_kernel import space_reg_ave, space_merge
from   pymir_kernel import resto_wiener
from   math import log
import os, sys, optparse
import readline # allow to back line in the shell
import cPickle, atexit

#=== constants ==================

listfun = ['exit', 'ls', 'rm', 'mv', 'cp', 'mem', 'save_var', 
           'load_var', 'add', 'fun', 'save_world', 'load_world',
           'ldir', 'load_im', 'save_im', 'show_mat', 'color2gray',
           'seq2mat', 'seq_reg_ave', 'load_vid', 'wiener', 'mosaicing']

B  = '\033[0;34m' # blue
BC = '\033[0;36m' # blue clear (or blue sky)
G  = '\033[0;32m' # green
GB = '\033[1;32m' # green bold
R  = '\033[0;31m' # red
RB = '\033[1;31m' # red bold
N  = '\033[m'     # neutral
Y  = '\033[0;33m' # yellow

sizebar = 32

# WORLD structure: WORLD['keyname'] = [header, data]
WORLD  = {}

# read history
readline.set_history_length(500)
histfile = os.path.join(os.environ["HOME"], ".astir_history")
try:
    readline.read_history_file(histfile)
except IOError:
    pass
# save always before exit, even when sys.exit is raised
atexit.register(readline.write_history_file, histfile)

#=== shell functions ============
def inbox_overwrite(name):
    answer = ''
    while answer != 'y' and answer != 'n':
        answer = raw_input('%s??%s Overwrite %s (%s[y]%s/%sn%s): '
                          % (Y, N, name, GB, N, R, N))
        if answer == '': answer = 'y'
    
    return answer

def inbox_question(message):
    answer = ''
    while answer != 'y' and answer != 'n':
        answer = raw_input('%s??%s %s (%s[y]%s/%sn%s): ' 
                          % (Y, N, message, GB, N, R, N))
        if answer == '': answer = 'y'
    
    return answer

def inbox_input(message):
    while 1:
        try:
            answer = raw_input('%s??%s %s ' % (Y, N, message))
            if answer == '':
                print '%s!!%s Again' % (B, N)
                continue
            break
        except:
            print '%s!!%s Again' % (B, N)
            continue

    return answer

def outbox_exist(name):
    print '%s!!%s %s doesn\'t exist' % (B, N, name)

def outbox_error(message):
    print '%sEE%s %s' % (R, N, message)

def outbox_bang(message):
    print '%s!!%s %s' % (B, N, message)

class progress_bar:
    def __init__(self, valmax, maxbar, title):
        if valmax == 0:  valmax = 1
        if maxbar > 200: maxbar = 200
        valmax -= 1
        self.valmax = valmax
        self.maxbar = maxbar
        self.title  = title

    def update(self, val):
        sys.stdout.flush()
        if val > self.valmax: val = self.valmax
        perc  = round((float(val) / float(self.valmax)) * 100)
        scale = 100.0 / float(self.maxbar)
        bar   = int(perc / scale)
        out   = '\r%s%s %s[%s%s%s%s] %s%3d %%%s' % (BC, self.title.ljust(10), G, Y, '=' * bar, ' ' * (self.maxbar - bar), G, RB, perc, N)
        sys.stdout.write(out)
        if perc == 100: sys.stdout.write('\n')

#=== cmd functions =============
def call_ls(args):
    '''
Listing all variables in work space
ls
    '''
    if len(args) > 0:
        print call_ls.__doc__
        return 0
    lname = WORLD.keys()
    lname.sort()
    space = 10 # cst columns size
    print '%s %s %s' % ('name'.ljust(space), 'type'.ljust(space), 'size'.ljust(space))
    for name in lname:
        kind = WORLD[name][0]
        if kind == 'var':
            print '%s %s%s %s%s%s' % (name.ljust(space), 
              G, 'var'.ljust(space), 
              R, ('[%i]' % len(WORLD[name][1])).ljust(space), N)
        elif kind == 'mat':
            mode = len(WORLD[name][1])
            h    = len(WORLD[name][1][0])
            w    = len(WORLD[name][1][0][0])
            if   mode == 1: mode = 'L'
            elif mode == 3: mode = 'RGB'
            else:           mode = 'RGBA'
            print '%s %s%s %s%s%s' % (name.ljust(space), 
              G, 'mat'.ljust(space), 
              R, '[%ix%i %s]' % (w, h, mode), N)
        elif kind == 'seq':
            nbm  = len(WORLD[name][1])
            mode = len(WORLD[name][1][0])
            h    = len(WORLD[name][1][0][0])
            w    = len(WORLD[name][1][0][0][0])
            if   mode == 1: mode = 'L'
            elif mode == 3: mode = 'RGB'
            else:           mode = 'RGBA'
            print '%s %s%s %s%s%s' % (name.ljust(space), 
              G, 'seq'.ljust(space), 
              R, '[%i mat %ix%i %s]' % (nbm, w, h, mode), N)
    return 1

def call_ldir(args):
    '''
Listing the current directory
ldir
    '''
    if len(args) > 0:
        print call_ldir.__doc__
        return 0

    os.system('ls')
    return 1

def call_rm(args):
    '''
Remove variables in work space
rm all
rm <name>
rm <name1> <name2> ...
rm <na*>
    '''
    if len(args) == 0 or args[0] == '-h':
        print call_rm.__doc__
        return 0
    if   args[0] == 'all': args = WORLD.keys()
    elif args[0].find('*') != -1:
        lname   = WORLD.keys()
        pattern = args[0].split('*')
        if len(pattern) != 2:
            outbox_error('Bad pattern')
            return -1
        args = []
        for name in lname:
            if name.find(pattern[0]) != -1 and name.find(pattern[1]) != -1:
                args.append(name)
        if len(args) == 0:
            outbox_error('No variable matchs with the pattern')
            return -1
        args.sort()
        outbox_bang('%i variables match with the pattern' % len(args))
        print args
        answer = inbox_question('Agree to remove all of them')
        if answer == 'n': return 0

    for name in args:
        try: del WORLD[name]
        except KeyError: outbox_exist(args[0])

    return 1

def call_mv(args):
    '''
Move/rename variables
mv <source_name> <target_name>
    '''
    if len(args) != 2 or args[0] == '-h':
        print call_mv.__doc__
        return 0
    try: data = WORLD[args[0]]
    except KeyError:
        outbox_exist(args[0])
        return -1
    keys = WORLD.keys()
    if args[1] in keys:
        answer = inbox_overwrite(args[1])
        if answer == 'n': return 0
    WORLD[args[1]] = data
    del WORLD[args[0]]
    del data

    return 1

def call_cp(args):
    '''
Copy variable
cp <source_name> <target_name>
    '''
    if len(args) == 0 or len(args) > 2 or args[0] == '-h':
        print call_cp.__doc__
        return 0
    try: data = WORLD[args[0]]
    except KeyError:
        outbox_exist(args[0])
        return -1
    keys = WORLD.keys()
    if args[1] in keys:
        answer = inbox_overwrite(args[1])
        if answer == 'n': return 0
    WORLD[args[1]] = data
    del data

    return 1

def call_mem(args):
    '''
Memories used in work space by the variables
mem
    '''
    if len(args) > 0:
        print call_mem.__doc__
        return 0
    space = 10
    txt = ['', 'k', 'M', 'G', 'T']
    lname = WORLD.keys()
    for name in lname:
        kind = WORLD[name][0]
        if   kind == 'var':
            size  = len(WORLD[name][1]) * 8
        elif kind == 'mat':
            mode = len(WORLD[name][1])
            h    = len(WORLD[name][1][0])
            w    = len(WORLD[name][1][0][0])
            size = mode * w * h * 4
        elif kind == 'seq':
            nbm  = len(WORLD[name][1])
            mode = len(WORLD[name][1][0])
            h    = len(WORLD[name][1][0][0])
            w    = len(WORLD[name][1][0][0][0])
            size = mode * w * h * nbm * 4
        ie    = int(log(size) // log(1e3))
        size /= (1e3 ** ie)
        size  = '%5.2f %sB' % (size, txt[ie])
        print '%s %s%s %s%s%s' % (name.ljust(space), 
              G, kind.ljust(space), 
              R, size.ljust(space), N)
        
    return 1

def call_fun(args):
    '''
Listing funtions available in Astir
fun
    '''
    if len(args) > 0:
        print call_fun.__doc__
        return 0
    listfun.sort()
    sfun = len(listfun)
    nc   = 3  # cst 3 columns
    if sfun % nc == 0: nl = sfun // nc
    else:              nl = (sfun // nc) + 1
    smax = 0
    for i in xrange(sfun):
        val = len(listfun[i])
        if val > smax: smax = val
    for i in xrange(nl):
        txt = ''
        for j in xrange(nc):
            ind = j * nl + i
            if ind < sfun: txt += '%s  ' % listfun[ind].ljust(smax)
            else:          txt += ''
        print txt

    return 1

def call_save_var(args):
    '''
Save Astir variable to file
save_var <var_name> <file_name>
    '''
    if len(args) != 2:
        print call_save_var.__doc__
        return 0
    lname = WORLD.keys()
    name  = args[0]
    fname = args[1]
    if name not in lname:
        outbox_exist(name)
        return -1
    lname = os.listdir('.')
    if fname in lname:
        answer = inbox_overwrite(fname)
        if answer == 'n': return 0
    f = open(fname, 'w')
    local = ['var_astir', name, WORLD[name]]
    cPickle.dump(local, f)
    f.close()

    return 1

def call_save_world(args):
    '''
Save the whole work space to a file
save_world <file_name>
    '''
    if len(args) == 0 or len(args) > 1 or args[0] == '-h':
        print call_save_world.__doc__
    kname = WORLD.keys()
    if len(kname) == 0:
        outbox_bang('Nothing to save')
        return 0
    fname = args[0]
    lname = os.listdir('.')
    if fname in lname:
        answer = inbox_overwrite(fname)
        if answer == 'n': return 0
    f = open(fname, 'w')
    local = ['world_astir', WORLD]
    cPickle.dump(local, f)
    f.close()
    
    return 1

def call_load_var(args):
    '''
Load variable fron file to work space
load_var <file_name>
    '''
    if len(args) == 0 or len(args) > 1 or args[0] == '-h':
        print call_load_var.__doc__
        return 0
    fname = args[0]
    lname = os.listdir('.')
    if fname not in lname:
        outbox_exist(fname)
        return -1
    f = open(fname, 'r')
    try: local = cPickle.load(f)
    except:
        outbox_error('Can not open the file')
        f.close()
        return -1
    f.close()
    if local[0] != 'var_astir':
        outbox_error('Not Astir format')
        return -1
    varname = local[1]
    vardata = local[2]
    lname   = WORLD.keys()
    while varname in lname:
        answer = inbox_overwrite(varname)
        if answer == 'n': varname = inbox_input('Change to a new name:')
        else: break
    WORLD[varname] = vardata

    return 1

def call_load_world(args):
    '''
Load a work space from a file
load_world <file_name>    
    '''
    if len(args) == 0 or len(args) > 1 or args[0] == '-h':
        print call_load_world.__doc__
        return 0
    fname = args[0]
    lname = os.listdir('.')
    if fname not in lname:
        outbox_exist(fname)
        return -1
    f = open(fname, 'r')
    try: local = cPickle.load(f)
    except:
        outbox_error('Can not open the file')
        f.close()
        return -1
    f.close()
    if local[0] != 'world_astir':
        outbox_error('Not Astir format')
        return -1
    answer = inbox_question('All variables will be deleted, are you agree')
    if answer == 'n': return 0
    del WORLD
    WORLD = local[1]

    return 1

def call_load_im(args):
    '''
Load images from files
Only one image
load_im <file_name.[bmp, jpg, png]>
Several images as a sequence
load_im <file_na*.png>
    '''
    if len(args) == 0 or len(args) > 1 or args[0] == '-h':
        print call_load_im.__doc__
        return 0
    if args[0].find('*') != -1:
        lname   = os.listdir('.')
        pattern = args[0].split('*')
        if len(pattern) != 2:
            outbox_error('Bad pattern')
            return -1
        mem = []
        for name in lname:
            if name.find(pattern[0]) != -1 and name.find(pattern[1]) != -1:
                mem.append(name)
        if len(mem) == 0:
            outbox_error('No image matchs with the pattern')
            return -1
        fname = mem[0]
        mem.sort()
        outbox_bang('%i files match with the pattern' % len(mem))
        print mem
        answer = inbox_question('Agree to load all of them')
        if answer == 'n': return 0
    else:
        mem   = None
        fname = args[0]

    buf = fname.split('.')
    if len(buf) == 2: name, ext = fname.split('.')
    else:             name, ext = None, None
    if ext not in ['bmp', 'jpg', 'png']:
        outbox_error('Bad extension (bmp, jpg or png)')
        return -1
    lname = os.listdir('.')
    if fname not in lname:
        outbox_exist(fname)
        return -1
    lname = WORLD.keys()
    while name in lname:
        answer = inbox_overwrite(name)
        if answer == 'n': name = inbox_input('Change to a new name:')
        else: break
    if mem is None:
        im  = image_read(fname)
        mat = image_im2mat(im)
        del im
        WORLD[name] = ['mat', mat]
        del mat
    else:
        bar  = progress_bar(len(mem), sizebar, 'loading')
        seq  = []
        name = mem[0].split('.')[0]
        i    = 0
        for item in mem:
            im  = image_read(item)
            mat = image_im2mat(im)
            seq.append(mat)
            bar.update(i)
            i += 1
        del im, mat
        WORLD[name] = ['seq', seq]
        del seq

    return 1

def call_save_im(args):
    '''
Save image from a variable to a file
save_im <mat_name> <file_name.[bmp, jpg, png]>
    '''
    if len(args) != 2:
        print call_save_im.__doc__
        return 0
    lname = WORLD.keys()
    name  = args[0]
    fname = args[1]
    if name not in lname:
        outbox_exist(name)
        return -1
    if WORLD[name][0] != 'mat':
        outbox_error('Only mat variable can be exported to image')
        return -1
    lext = ['jpg', 'png', 'bmp']
    ext = 'png'
    if len(fname.split('.')) != 2:
        outbox_bang('Must have an extension, set default to png')
        ext = 'png'
    else:
        [fname, ext] = fname.split('.')
        if ext not in lext:
            outbox_error('Wrong extension, only jpg, png, or bmp')
            return -1
    fname = fname + '.' + ext
    lname = os.listdir('.')
    if fname in lname:
        answer = inbox_overwrite(fname)
        if answer == 'n': return 0
    mat = WORLD[name][1]
    im  = image_mat2im(mat)
    del mat
    image_write(im, fname)
    del im

    return 1

def call_show_mat(args):
    '''
Display a mat variable as an image
show_mat <mat_name>
Display a grid on the image
show_mat <mat_name> g[size_inter_grid_in_pixel]
    '''
    if len(args) == 0 or len(args) > 2 or args[0] == '-h':
        print call_show_mat.__doc__
        return 0
    lname = WORLD.keys()
    name  = args[0]
    if name not in lname:
        outbox_exist(name)
        return -1
    if WORLD[name][0] != 'mat':
        outbox_error('Only mat variable can be displayed')
        return -1
    mat = WORLD[name][1]
    im  = image_mat2im(mat)
    if len(args) > 1:
        if args[1][0] != 'g':
            outbox_error('Argument %s incorrect' % args[1])
            return -1
        else:
            try: g = int(args[1][1:])
            except:
                outbox_error('Argument %s incorrect' % args[1])
                return -1
            if g < 1 or g > 200:
                outbox_error('Argument g incorrect [1; 200]')
                return -1
            image_show_grid(im, g)
            del g
    else:
        image_show(im)
        del im, mat

    return 1

def call_color2gray(args):
    '''
Convert mat color (RGB or RGBA) to gray scale (Luminance)
Convert in-place
color2gray <mat_name>
Convert to new mat
color2gray <mat_name> <mat_new_name>
Convert a mat sequence in-place
color2gray <seq_name>
Convert a mat sequence to a new one
color2gray <seq_name> <seq_new_name>
    '''
    if len(args) == 0 or len(args) > 2 or args[0] == '-h':
        print call_color2gray.__doc__
        return 0
    lname = WORLD.keys()
    src   = args[0]
    if src not in lname:
        outbox_exist(src)
        return -1
    kind  = WORLD[src][0]
    if kind not in ['mat', 'seq']:
        outbox_error('Only mat or seq variable can be converted')
        return -1
    if kind == 'mat':
        if len(WORLD[src][1]) == 1:
            outbox_error('Already in gray scale')
            return -1
        if len(args) == 2:
            trg = args[1]
            while trg in lname:
                answer = inbox_overwrite(trg)
                if answer == 'n': trg == inbox_input('Change to a new name:')
                else: break
        else: trg = src

        im  = image_mat2im(WORLD[src][1])
        im  = color_color2gray(im)
        mat = image_im2mat(im)
        WORLD[trg] = ['mat', mat]

    else:
        if len(WORLD[src][1][0]) == 1:
            outbox_error('Already in gray scale')
            return -1
        if len(args) == 2:
            trg = args[1]
            while trg in lname:
                answer = inbox_overwrite(trg)
                if answer == 'n': trg == inbox_input('Change to a new name:')
                else: break
        else: trg = src

        nb   = len(WORLD[src][1])
        bar  = progress_bar(nb, sizebar, 'Processing')
        data = []
        for n in xrange(nb):
            im  = image_mat2im(WORLD[src][1][n])
            im  = color_color2gray(im)
            mat = image_im2mat(im)
            data.append(mat)
            bar.update(n)
        WORLD[trg] = ['seq', data]
        del data

    del mat, im

    return 1

def call_seq2mat(args):
    '''
Extract mat variables from a sequence
Only one
seq2mat <seq_name> 5 <basename_mat>
Or several mat, in this case 3 mats
seq2mat <seq_name> 2:4 <basename_mat>
Or all mat store in the sequence
seq2mat <seq_name> all <basename_mat>
new mat name = <basename_mat> + index (format 000)
% seq2mat test 2 res
res002
    '''
    if len(args) != 3 or args[0] == '-h':
        print call_seq2mat.__doc__
        return 0
    lname = WORLD.keys()
    src   = args[0]
    id    = args[1]
    trg   = args[2]
    if src not in lname:
        outbox_exist(src)
        return -1
    if WORLD[src][0] != 'seq':
        outbox_error('Only seq variable can be converted')
        return -1
    id   = id.split(':')
    size = len(WORLD[src][1])
    if len(id) == 1:
        if id[0] == 'all':
            id = range(size)
        else:
            try: id = int(id[0])
            except:
                outbox_error('Range value incorrect')
                return -1
            if id < 0 or id >= size:
                outbox_error('Value is out of range [0, %i]' % size)
                return -1
            while trg in lname:
                answer = inbox_overwrite(trg)
                if answer == 'n': trg == inbox_input('Change to a new name')
                else: break
            mat = WORLD[src][1][id]
            WORLD[trg] = ['mat', mat]
            return 1
    else:
        try: start, stop = int(id[0]), int(id[1])
        except:
            outbox_error('Range value incorrect')
            return -1
        if start < 0 or stop >= size:
            outbox_error('Values are out of range [0, %i]' % size)
            return -1
        id = range(start, stop + 1)

    for i in id:
        mat = WORLD[src][1][i]
        WORLD[trg + '%03i' % i] = ['mat', mat]

    return 1

def call_seq_reg_ave(args):
    '''
This function use a simple registration to match images together
and compute the averages. The sequence of matrices must be in gray scale.

seq_reg_ave <seq_name> <dx> <dy> <ws>

dx: is the translation range search on x (x-dx to x+dx)
dy: is the translation range search on y (y-dy to y+dy)
ws: window size used to track translation between images (must be odd)

seq_reg_ave im 10 10 35
    '''
    if len(args) != 4:
        print call_seq_reg_ave.__doc__
        return 0
    lname = WORLD.keys()
    src   = args[0]
    if src not in lname:
        outbox_exist(src)
        return -1
    kind = WORLD[src][0]
    if kind != 'seq':
        outbox_error('Only seq variable can be used')
        return -1
    dx = int(args[1])
    dy = int(args[2])
    ws = int(args[3])
    if ws % 2 == 0:
        ws += 1
        outbox_bang('Window size must be odd, set to %i' % ws)
    mat = WORLD[src][1][0]
    im  = image_mat2im(mat)
    p   = image_show_get_pts(im, 1)
    print 'point selected:', p[0]
    dw  = (ws - 1) // 2
    x   = p[0][1]
    y   = p[0][0]
    l1  = [[y-dw, x-dw], [y-dw, x+dw], [y+dw, x+dw], [y+dw, x-dw]]
    l2  = [[y+dw, x-dw], [y-dw, x-dw], [y-dw, x+dw], [y+dw, x+dw]]
    im  = color_gray2color(im)
    im  = image_plot_lines(im, l1, l2, 'red')
    im  = image_plot_points(im, p, 'pixel')
    image_show(im)
    ave = space_reg_ave(WORLD[src][1], p, ws, dx, dy)
    WORLD['ave_' + src] = ['mat', ave]
    return 1

def call_load_vid(args):
    '''
Load video (avi file only) to a sequence
load_vid <video_name> <frame_per_second>
    '''
    if len(args) != 2:
        print call_load_vid.__doc__
        return 0
    lname    = os.listdir('.')
    filename = args[0]
    freq     = int(args[1])
    if filename not in lname:
        outbox_exist(filename)
        return -1
    name, ext = filename.split('.')
    if ext != 'avi':
        outbox_error('Must be an avi file')
        return -1
    lname = WORLD.keys()
    while name in lname:
        answer = inbox_overwrite(name)
        if answer == 'n': name = inbox_input('Change to a new name:')
        else: break
    print 'Extract images...'
    pattern = '.tmp_astir_'
    try:
        os.system('ffmpeg -i %s -r %i -f image2 "%s%%4d.png"' % (filename, freq, pattern))
    except:
        outbox_error('Impossible to extract images from the video')
        return -1
    lname = os.listdir('.')
    mem   = []
    for file in lname:
        if file.find(pattern) != -1: mem.append(file)
    bar = progress_bar(len(mem), sizebar, 'loading')
    seq = []
    i   = 0
    for item in mem:
        im  = image_read(item)
        mat = image_im2mat(im)
        seq.append(mat)
        bar.update(i)
        i += 1
    del im, mat
    WORLD[name] = ['seq', seq]
    del seq
    os.system('rm -f %s*' % pattern)
    
    return 1

def call_wiener(args):
    '''
Image restoration by Wiener filter
wiener <mat_source_name> <mat_res_name>
    '''
    if len(args) != 2:
        print call_wiener.__doc__
        return 0
    src   = args[0]
    trg   = args[1]
    lname = WORLD.keys()
    if src not in lname:
        outbox_exist(src)
        return -1
    if trg in lname:
        answer = inbox_overwrite(trg)
        if answer == 'n': return 0
    if WORLD[src][0] != 'mat':
        outbox_error('Only mat variable can be used')
        return -1
    res = resto_wiener(WORLD[src][1])
    WORLD[trg] = ['mat', res]

    return 1

def call_mosaicing(args):
    '''
Create mosaicing from two images
mosaicing <mat_1> <mat_2>
    '''
    mat1 = WORLD[args[0]][1]
    mat2 = WORLD[args[1]][1]
    ws   = 35

    im  = image_mat2im(mat1)
    p1  = image_show_get_pts(im, 1)
    print 'point selected:', p1[0]
    dw  = (ws - 1) // 2
    x   = p1[0][1]
    y   = p1[0][0]
    l1  = [[y-dw, x-dw], [y-dw, x+dw], [y+dw, x+dw], [y+dw, x-dw]]
    l2  = [[y+dw, x-dw], [y-dw, x-dw], [y-dw, x+dw], [y+dw, x+dw]]
    im  = color_gray2color(im)
    im  = image_plot_lines(im, l1, l2, 'red')
    im  = image_plot_points(im, p1, 'pixel')
    image_show(im)

    im  = image_mat2im(mat2)
    p2  = image_show_get_pts(im, 1)
    print 'point selected:', p2[0]
    dw  = (ws - 1) // 2
    x   = p2[0][1]
    y   = p2[0][0]
    l1  = [[y-dw, x-dw], [y-dw, x+dw], [y+dw, x+dw], [y+dw, x-dw]]
    l2  = [[y+dw, x-dw], [y-dw, x-dw], [y-dw, x+dw], [y+dw, x+dw]]
    im  = color_gray2color(im)
    im  = image_plot_lines(im, l1, l2, 'red')
    im  = image_plot_points(im, p2, 'pixel')
    image_show(im)

    from pymir_kernel import space_align 
    xp, yp = space_align(mat1[0], mat2[0], p1, 35, 5, 5, p2)
    print xp, yp

    res = space_merge(mat1, mat2, [yp, xp])
    WORLD['res'] = ['mat', res]

    return 1

'''
#=== documentation ==============
print call_ls.__doc__
print call_ldir.__doc__
print call_rm.__doc__
print call_mv.__doc__
print call_cp.__doc__
print call_mem.__doc__
print call_fun.__doc__
print call_save_var.__doc__
print call_save_world.__doc__
print call_load_var.__doc__
print call_load_world.__doc__
print call_load_im.__doc__
print call_save_im.__doc__
print call_show_mat.__doc__
print call_color2gray.__doc__
print call_seq2mat.__doc__
print call_seq_reg_ave.__doc__
print call_load_vid.__doc__
print call_wiener.__doc__
print call_mosaicing.__doc__
sys.exit()
'''

#=== shell io ===================

# script kernel
script_flag = False
script_end  = False
if len(sys.argv) != 1:
    script_name = sys.argv[1]
    dummy, ext  = script_name.split('.')
    if ext != 'sas':
        outbox_error('This file %s is not a Script Astir Shell (.sas).' % script_name)
        sys.exit()
    script_flag = True
    list_cmd = open(script_name, 'r').readlines()

# if mode shell
if script_flag:
    print '** Script Astir Shell V1.0 **'
else:
    print '  ___      _   _'
    print ' / _ \    | | (_)'         
    print '/ /_\ \___| |_ _ _ __' 
    print '|  _  / __| __| | \'__)'
    print '| | | \__ \ |_| | |'
    print '\_| |_/___/\__|_|_|'

    print '** Astir Shell V1.0 **\n'


ct_cmd = 1
while 1 and not script_end:
    if script_flag:
        cmd = list_cmd[ct_cmd - 1]
        if cmd[0] == '#':
            ct_cmd += 1
            continue
        print '%s%s%s' % (B, cmd.strip('\n'), N)
        if ct_cmd == len(list_cmd):
            script_end = True
    else:
        try: cmd = raw_input('%sastir%s %i%s %%%s ' % (B, GB, ct_cmd, G, N))
        except:
            print '\nbye'
            sys.exit(0)

    if not cmd: continue

    ct_cmd   += 1
    parse     = cmd.split()
    progname  = parse[0]
    args      = parse[1:]

    if progname not in listfun:
        try: print eval(cmd)
        except:
            outbox_bang(' 8-/')
            continue
            
    #=== parser and caller ======

    #=== basic functions
    if progname == 'exit':
        print 'bye'
        sys.exit(0)
    if progname == 'ls':
        call_ls(args)
        continue
    if progname == 'ldir':
        call_ldir(args)
        continue
    if progname == 'rm':
        call_rm(args)
        continue
    if progname == 'mv':
        call_mv(args)
        continue       
    if progname == 'cp':
        call_cp(args)
        continue
    if progname == 'mem':
        call_mem(args)
        continue
    if progname == 'fun':
        call_fun(args)
        continue
    #=== input/output cmd
    if progname == 'save_var':
        call_save_var(args)
        continue
    if progname == 'save_world':
        call_save_world(args)
        continue
    if progname == 'load_var':
        call_load_var(args)
        continue
    if progname == 'load_world':
        call_load_world(args)
        continue
    ## TO DEBUG
    if progname == 'add':
        name = args[0]
        size = int(args[1])
        V = [0] * size
        WORLD[name] = ['var', V]
        continue
    #=== Pymir command
    if progname == 'load_im':
        call_load_im(args)
        continue
    if progname == 'save_im':
        call_save_im(args)
        continue
    if progname == 'load_vid':
        call_load_vid(args)
        continue
    if progname == 'show_mat':
        call_show_mat(args)
        continue
    if progname == 'color2gray':
        call_color2gray(args)
        continue
    if progname == 'seq2mat':
        call_seq2mat(args)
        continue    
    if progname == 'seq_reg_ave':
        call_seq_reg_ave(args)
        continue
    if progname == 'wiener':
        call_wiener(args)
        continue

    if progname == 'mosaicing':
        call_mosaicing(args)
        continue
