#!/usr/bin/env python
import os, sys
import readline # allow to back line in the shell

#=== constants =================

listfun = ['exit', 'ls', 'rm', 'mv', 'cp', 'mem', 'save_var', 
           'load_var', 'add', 'fun', 'save_world', 'load_world',
           'ldir']

B  = '\033[0;34m' # blue
G  = '\033[0;32m' # green
GB = '\033[1;32m' # green bold
R  = '\033[0;31m' # red
N  = '\033[m'     # neutral
Y  = '\033[0;33m' # yellow

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
        answer = raw_input('%s??%s %s (%s[y]%s/%smn%s): ' 
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

#=== shell ======================
WORLD = {}
ct_cmd = 1

print '  ___      _   _'
print ' / _ \    | | (_)'         
print '/ /_\ \___| |_ _ _ __' 
print '|  _  / __| __| | \'__)'
print '| | | \__ \ |_| | |'
print '\_| |_/___/\__|_|_|'

print '** Astir Shell V1.0 **\n'

while 1:
    try: cmd = raw_input('%sastir%s %i%s %%%s ' % (B, GB, ct_cmd, G, N)).split()
    except:
        print 'bye'
        sys.exit(0)

    if not cmd: continue

    ct_cmd   += 1
    progname  = cmd[0]
    args      = cmd[1:]

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
            print '%s %s%s %s%s%s' % (name.ljust(space), 
                  G, 'mat'.ljust(space), 
                  R, ('[%i]' % len(WORLD[name])).ljust(space), N)
        continue

    if progname == 'ldir':
        if len(args) > 0:
            print '## listing of the current directory'
            print '#  ldir'
            continue
        import os
        #list = os.listdir('.')
        #print list
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
        from math import log
        txt = ['', 'k', 'M', 'G', 'T']
        lname = WORLD.keys()
        for name in lname:
            size  = len(WORLD[name]) * 4
            ie    = int(log(size) // log(1e3))
            size /= (1e3 ** ie)
            size  = '%5.2f %sB' % (size, txt[ie])
            print name, size
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
        if len(args) == 0 or len(args) > 2 or args[0] == '-h':
            print '## save variable to file'
            print '#  save_var <var> <filename>'
            continue
        import cPickle
        lname = WORLD.keys()
        name  = args[0]
        fname = args[1]
        if name not in lname:
            outbox_exist(name)
            continue
        import os
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
        import cPickle
        kname = WORLD.keys()
        if len(kname) == 0:
            outbox_bang('Nothing to save')
            continue
        import os
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
        import cPickle
        fname = args[0]
        import os
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
        import cPickle
        fname = args[0]
        import os
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
        WORLD[name] = V
        
