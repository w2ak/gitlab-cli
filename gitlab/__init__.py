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

# BEGIN __init__.py
from . import config,api

@logged
def init(log):
    api.set_config(\
            url=config.get('server.url'),
            token=config.get('server.token',secret=True)
        )
# END __init__.py
