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
from argparse import ArgumentParser
from . import cli_functions as cli

def parse_args():
    getter_setter=ArgumentParser(add_help=False)
    getter_setter.add_argument('key',default=None,nargs='?')
    getter_setter.add_argument('value',default=None,nargs='?')

    ap = ArgumentParser(prog='gitlab')
    ap.set_defaults(action=lambda args: ap.print_help())

    ap_= ap.add_subparsers(help='Command')

    # gitlab config [--local|--global] [key [value]]
    config = ap_.add_parser('config',\
            help='Configuration management.',\
            parents=[getter_setter])
    config.set_defaults(action=cli.config)
    config.add_argument('--local',dest='config',action='store_const',
            const='local',default=None)
    config.add_argument('--global',dest='config',action='store_const',
            const='global')

    # gitlab me [key [value]]
    me = ap_.add_parser('me',\
            help='Get your information',\
            parents=[getter_setter])
    me.set_defaults(action=cli.me)
    return ap.parse_args()

@logged
def run(log):
    args = parse_args()
    args.action(args)
# END cli.py
