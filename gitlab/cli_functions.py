# LOGGING HEADER
import logging,sys,os
logger=logging.getLogger(\
        os.path.basename(sys.argv[0]) if __name__=='__main__'
        else __name__)
def logged(f):
    log=logger.getChild(f.__name__)
    def g(*args,**kwargs):
        log.debug('in')
        result=f(log,*args,**kwargs)
        log.debug('out')
        return result
    g.__name__=f.__name__
    return g

# BEGIN cli_functions.py
from requests import codes as http
from json import dump as jdump
from . import api,init,config

"""
CLI messages
"""
def error(msg,*args,**kwargs):
    sys.stderr.write('error: {:}\n'.format(\
            msg.format(*args,**kwargs)))
    sys.exit(1)
def http_error(code,reason):
    error('http [{:}] {:}',code,reason)

"""
Wrappers
"""
def getter_setter(g,s):
    def f(args):
        if args.value is None:
            return g(args)
        return s(args)
    return f

"""
User information
"""
def get_me(args):
    init()
    status, reason, me = api.get_user()
    if status != http.ok:
        http_error(status, reason)
    if args.key is None:
        jdump(me, sys.stdout, sort_keys=True, indent=2)
        sys.stdout.write('\n')
        sys.stdout.flush()
        return
    if args.key in me:
        sys.stdout.write('{:}\n'.format(me[args.key]))
        sys.stdout.flush()
        return
    error("no such field: {:}".format(args.key))
def set_me(args):
    raise NotImplementedError('set_me')
me=getter_setter(get_me,set_me)

"""
Configuration information
"""
def get_config(args):
    cfg=config.get()
    if args.key is None:
        for s,S in cfg.items():
            for k,v in S.items():
                print('{:}.{:}={:}'.format(s,k,v))
    else:
        keys=args.key.split('.')
        if len(keys)<2:
            cli_error("key does not contain a section: '{:}'",
                    args.key)
        if len(keys)>2:
            cli_error("configuration does not support subsections: '{:}'",
                    args.key)
        v = cfg.get(*keys,fallback=None)
        if v is None:
            cli_error("no such configuration entry: '{:}'",
                    args.key)
        print('{:}.{:}={:}'.format(*keys,v))
def set_config(args):
    raise NotImplementedError('set_config')
config=getter_setter(get_config,set_config)
# END cli_functions.py
