#!/usr/bin/env python
#=== import =====================

from   pymir_kernel import image_read, image_write
from   pymir_kernel import image_im2mat, image_mat2im
from   pymir_kernel import image_show
from   math import log
import os, sys
import readline # allow to back line in the shell
import cPickle

#=== constants ==================

listfun = ['exit', 'ls', 'rm', 'mv', 'cp', 'mem', 'save_var', 
           'load_var', 'add', 'fun', 'save_world', 'load_world',
           'ldir', 'load_im', 'save_im', 'show_mat']

B  = '\033[0;34m' # blue
BC = '\033[0;36m' # blue clear (or blue sky)
G  = '\033[0;32m' # green
GB = '\033[1;32m' # green bold
R  = '\033[0;31m' # red
RB = '\033[1;31m' # red bold
N  = '\033[m'     # neutral
Y  = '\033[0;33m' # yellow

sizebar = 32

#=== functions =================
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

#=== shell ======================

# WORLD structure: WORLD['keyname'] = [header, data]
WORLD  = {}
ct_cmd = 1
'''
print '  ___      _   _'
print ' / _ \    | | (_)'         
print '/ /_\ \___| |_ _ _ __' 
print '|  _  / __| __| | \'__)'
print '| | | \__ \ |_| | |'
print '\_| |_/___/\__|_|_|'

print '** Astir Shell V1.0 **\n'
'''
while 1:
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
            
    #=== shell function =========
    if progname == 'exit':
        print 'bye'
        sys.exit(0)
    
    if progname == 'ls':
        if len(args) > 0:
            print '## listing of all variables'
            print '#  ls'
            continue
        lname = WORLD.keys()
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
        continue

    if progname == 'ldir':
        if len(args) > 0:
            print '## listing of the current directory'
            print '#  ldir'
            continue
        os.system('ls')
        continue

    if progname == 'rm':
        if len(args) == 0 or args[0] == '-h':
            print '## remove variable'
            print '#  rm all'
            print '#  rm <name>'
            print '#  rm <name> <name> ...'
            continue
        if args[0] == 'all': args = WORLD.keys()
        for name in args:
            try: del WORLD[name]
            except KeyError: outbox_exist(args[0])
        continue

    if progname == 'mv':
        if len(args) == 0 or len(args) > 2 or args[0] == '-h':
            print '## move variable'
            print '#  mv <source_name> <target_name>'
            continue
        try: data = WORLD[args[0]]
        except KeyError:
            outbox_exist(args[0])
            continue
        keys = WORLD.keys()
        if args[1] in keys:
            answer = inbox_overwrite(args[1])
            if answer == 'n': continue
        WORLD[args[1]] = data
        del WORLD[args[0]]
        del data
        continue                

    if progname == 'cp':
        if len(args) == 0 or len(args) > 2 or args[0] == '-h':
            print '## copy variable'
            print '#  cp <source_name> <target_name>'
            continue
        try: data = WORLD[args[0]]
        except KeyError:
            outbox_exist(args[0])
            continue
        keys = WORLD.keys()
        if args[1] in keys:
            answer = inbox_overwrite(args[1])
            if answer == 'n': continue
        WORLD[args[1]] = data
        del data
        continue
    
    if progname == 'mem':
        if len(args) > 0:
            print '## memories for all variables'
            print '#  mem'
            continue
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

        continue

    if progname == 'fun':
        if len(args) > 0:
            print '## listing of functions in Astir'
            print '#  fun'
            continue
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

        continue

    #=== input/output cmd =======
    if progname == 'save_var':
        if len(args) != 2:
            print '## save variable to file'
            print '#  save_var <var> <filename>'
            continue
        lname = WORLD.keys()
        name  = args[0]
        fname = args[1]
        if name not in lname:
            outbox_exist(name)
            continue
        lname = os.listdir('.')
        if fname in lname:
            answer = inbox_overwrite(fname)
            if answer == 'n': continue
        f = open(fname, 'w')
        local = ['var_astir', name, WORLD[name]]
        cPickle.dump(local, f)
        f.close()
        continue
    
    if progname == 'save_world':
        if len(args) == 0 or len(args) > 1 or args[0] == '-h':
            print '## save all variables in the same file'
            print '#  save_world <filename>'
            continue
        kname = WORLD.keys()
        if len(kname) == 0:
            outbox_bang('Nothing to save')
            continue
        fname = args[0]
        lname = os.listdir('.')
        if fname in lname:
            answer = inbox_overwrite(fname)
            if answer == 'n': continue
        f = open(fname, 'w')
        local = ['world_astir', WORLD]
        cPickle.dump(local, f)
        f.close()
        continue

    if progname == 'load_var':
        if len(args) == 0 or len(args) > 1 or args[0] == '-h':
            print '## load variable from file'
            print '#  load_var <filename>'
            continue
        fname = args[0]
        lname = os.listdir('.')
        if fname not in lname:
            outbox_exist(fname)
            continue
        f = open(fname, 'r')
        try: local = cPickle.load(f)
        except:
            outbox_error('Can not open the file')
            f.close()
            continue
        f.close()
        if local[0] != 'var_astir':
            outbox_error('Not Astir format')
            continue
        varname = local[1]
        vardata = local[2]
        lname   = WORLD.keys()
        while varname in lname:
            answer = inbox_overwrite(varname)
            if answer == 'n': varname = inbox_input('Change to a new name:')
            else: break
        WORLD[varname] = vardata
        continue

    if progname == 'load_world':
        if len(args) == 0 or len(args) > 1 or args[0] == '-h':
            print '## load all variables from file'
            print '#  load_world <filename>'
            continue
        fname = args[0]
        lname = os.listdir('.')
        if fname not in lname:
            outbox_exist(fname)
            continue
        f = open(fname, 'r')
        try: local = cPickle.load(f)
        except:
            outbox_error('Can not open the file')
            f.close()
            continue
        f.close()
        if local[0] != 'world_astir':
            outbox_error('Not Astir format')
            continue
        answer = inbox_question('All variables will be deleted, are you agree')
        if answer == 'n': continue
        del WORLD
        WORLD = local[1]
        continue

    if progname == 'add':
        name = args[0]
        size = int(args[1])
        V = [0] * size
        WORLD[name] = ['var', V]
        continue

    #=== Pymir command =========
    if progname == 'load_im':
        if len(args) == 0 or len(args) > 1 or args[0] == '-h':
            print '## load image from file'
            print '#  Pymir function'
            print '#  load_im <filename.[bmp, jpg, png]>'
            print '#  load_im <filen*.bmp>'
            continue

        if args[0].find('*') != -1:
            lname  = os.listdir('.')
            pattern = args[0].split('*')
            if len(pattern) != 2:
                outbox_error('Bad pattern')
                continue
            mem = []
            for name in lname:
                if name.find(pattern[0]) != -1 and name.find(pattern[1]) != -1:
                    mem.append(name)
            if len(mem) == 0:
                outbox_error('No image matchs with the pattern')
                continue
            fname = mem[0]
            mem.sort()
            outbox_bang('%i files match with the pattern' % len(mem))
            print mem
            answer = inbox_question('Agree to load all of them')
            if answer == 'n': continue
        else:
            mem   = None
            fname = args[0]

        name, ext = fname.split('.')
        if ext not in ['bmp', 'jpg', 'png']:
            outbox_error('Bad extension (bmp, jpg or png)')
            continue
        lname = os.listdir('.')
        if fname not in lname:
            outbox_exist(fname)
            continue
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
        continue

    if progname == 'save_im':
        if len(args) != 2:
            print '## save image to file'
            print '#  save_im <mat> <filename>'
            continue
        lname = WORLD.keys()
        name  = args[0]
        fname = args[1]
        if name not in lname:
            outbox_exist(name)
            continue
        if WORLD[name][0] != 'mat':
            outbox_error('Only mat variable can be exported to image')
            continue
        lext = ['jpg', 'png', 'bmp']
        ext = 'png'
        if len(fname.split('.')) != 2:
            outbox_bang('Must have an extension, set default to png')
            ext = 'png'
        else:
            [fname, ext] = fname.split('.')
            if ext not in lext:
                outbox_error('Wrong extension, only jpg, png, or bmp')
                continue
        fname = fname + '.' + ext
        lname = os.listdir('.')
        if fname in lname:
            answer = inbox_overwrite(fname)
            if answer == 'n': continue
        mat = WORLD[name][1]
        im  = image_mat2im(mat)
        del mat
        image_write(im, fname)
        del im
        continue

    if progname == 'show_mat':
        if len(args) != 1:
            print '## display mat as image'
            print '#  show_mat <mat>'
            continue
        lname = WORLD.keys()
        name  = args[0]
        if name not in lname:
            outbox_exist(name)
            continue
        if WORLD[name][0] != 'mat':
            outbox_error('Only mat variable can be displayed')
            continue
        mat = WORLD[name][1]
        im  = image_mat2im(mat)
        image_show(im)
        del im, mat
        continue
