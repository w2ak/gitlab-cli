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

# BEGIN cli.py
from requests import codes as http
from json import dump as jdump
from argparse import ArgumentParser
from . import api,init,config

"""
CLI messages
"""
def cli_error(msg,*args,**kwargs):
    sys.stderr.write('error: {:}\n'.format(\
            msg.format(*args,**kwargs)))
    sys.exit(1)
def http_error(code,reason):
    cli_error('http [{:}] {:}',code,reason)

def get_me(args):
    init()
    status, reason, me = api.get_user()
    if status != http.ok:
        http_error(status, reason)
    jdump(me, sys.stdout, sort_keys=True, indent=2)
    sys.stdout.write('\n')
    sys.stdout.flush()

def cli_config(args):
    print(args)
    if args.value is None:
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
    else:
        raise NotImplementedError('config.set')

def parse_args():
    ap = ArgumentParser(prog='gitlab')
    ap.set_defaults(action=lambda args: ap.print_help())

    ap_= ap.add_subparsers(help='Command')

    config = ap_.add_parser('config',\
            help='Configuration management.')
    config.set_defaults(action=cli_config)

    config.add_argument('--local',dest='config',action='store_const',
            const='local',default=None)
    config.add_argument('--global',dest='config',action='store_const',
            const='global')
    config.add_argument('key',default=None,nargs='?')
    config.add_argument('value',default=None,nargs='?')

    me = ap_.add_parser('me',\
            help='Get your information')
    me.set_defaults(action=get_me)
    return ap.parse_args()

@logged
def run(log):
    args = parse_args()
    args.action(args)
# END cli.py
