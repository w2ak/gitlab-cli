#!/usr/bin/env python3
# LOGGING HEADER
import logging,sys,os
logger=logging.getLogger(\
        'gitlab' if __name__=='__main__'
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
from . import config,api

"""
Logging level setup
"""
logging.basicConfig(level=logging.INFO)
# logging.getLogger('gitlab').setLevel(logging.DEBUG)
# logging.getLogger('gitlab.config').setLevel(logging.DEBUG)
logging.getLogger('gitlab.api').setLevel(logging.DEBUG)

def parse_args():
    ap = argparse.ArgumentParser()
    return ap.parse_args()

@logged
def main(log,args):
    api.set_config(\
            url=config.get('server.url'),
            token=config.get('server.token',secret=True)
        )
    me=api.user()
    log.info(me.json())

if __name__=='__main__':
    args = parse_args()
    main(args)
# END gitlab.py
