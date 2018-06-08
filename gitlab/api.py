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

# BEGIN api.py
import requests

__api_base_path='/api/v4'
__api_base_url=None
__api_private_token=None
@logged
def set_config(log,**kwargs):
    global __api_base_url
    abu=kwargs.get('url',None)
    if abu is not None:
        log.info('url => {:}'.format(abu))
        __api_base_url=abu
    global __api_private_token
    apt=kwargs.get('token',None)
    if apt is not None:
        log.info('token => ********'.format(apt))
        __api_private_token=apt
@logged
def get_url(log,api_path):
    if __api_base_url is None:
        log.critical('No base URL in config: server.url!')
        raise KeyError('api_base_url')
    return '{:}{:}{:}'.format(__api_base_url,__api_base_path,api_path)
@logged
def get_headers(log):
    hdr=dict()
    if __api_private_token is None:
        log.warning('No private token.')
    else:
        hdr['Private-Token']=__api_private_token
        log.debug('Private-Token:*****')
    return hdr

"""
Actual API calls
"""
@logged
def get_user(log):
    url=get_url('/user')
    hdr=get_headers()
    res=requests.get(url,headers=hdr)
    return res.status_code,res.reason,res.json()

@logged
def get_users(log,username=None):
    url=get_url('/users')
    hdr=get_headers()
    pld=dict()
    if username is not None:
        pld['username']=username
    # data=pld or params=pld
    res=requests.get(url,headers=hdr,data=pld)
    return res.status_code,res.reason,res.json()
# END api.py
