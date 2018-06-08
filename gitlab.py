#!/usr/bin/env python3
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

# BEGIN gitlab.py
import argparse
from gitlab import config

"""
Logging level setup
"""
logging.basicConfig(level=logging.INFO)
# logging.getLogger('gitlab').setLevel(logging.DEBUG)
# logging.getLogger('gitlab.config').setLevel(logging.DEBUG)

def parse_args():
    ap = argparse.ArgumentParser()
    return ap.parse_args()

@logged
def main(log,args):
    url=config.get('server.url')

if __name__=='__main__':
    args = parse_args()
    main(args)
# END gitlab.py
