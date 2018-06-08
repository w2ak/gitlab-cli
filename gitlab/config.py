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

# BEGIN config.py
from io import StringIO
from configparser import ConfigParser,ExtendedInterpolation
from subprocess import run,PIPE

__config_filename = 'gitlab.ini'
__config = None

"""
Configuration file access checker
"""
__rights={ 'r': os.R_OK, 'w': os.W_OK, 'x': os.X_OK }
@logged
def parse_rights(log,rights):
    num_rights=0
    for x in rights:
        num_rights|=__rights.get(x.lower(),0)
    log.debug('{:} -> {:}'.format(rights,num_rights))
    return num_rights
@logged
def format_rights(log,num_rights):
    rights=''
    for x in ['r','w','x']:
        rights+= x if num_rights&__rights.get(x,0) else '-'
    log.debug('{:} -> {:}'.format(num_rights,rights))
    return rights
@logged
def check_cfg(log,filename,rights='r'):
    nr=parse_rights(rights)
    if os.access(filename,nr):
        log.info('{:}:{:}:OK'.format(filename,format_rights(nr)))
        return filename
    log.warning('{:}:{:}:KO'.format(filename,format_rights(nr)))
    return None

"""
Folder finding
"""
@logged
def get_git_dir(log):
    ggd=['git','rev-parse','--git-dir']
    out=run(ggd,stdout=PIPE)
    if out.returncode == 0:
        path=out.stdout.decode('utf-8').strip()
        path=os.path.abspath(path)
        log.info(path)
        return path
    log.warning('{:}:Not in a git repository.'.format(os.getenv('PWD')))
    return None

"""
Configuration filename computation
"""
__config_filename_getters=list()
def new_config_filename_getter(f):
    __config_filename_getters.append(f)
@new_config_filename_getter
@logged
def get_system_cfg(log):
    filename=os.path.join('/etc',__config_filename)
    return check_cfg(filename)
@new_config_filename_getter
@logged
def get_home_Xcfg(log):
    home=os.getenv('HOME')
    if home:
        filename=os.path.join(home,'.config',__config_filename)
        return check_cfg(filename)
    log.error('No HOME variable!')
    return None
@new_config_filename_getter
@logged
def get_home_cfg(log):
    home=os.getenv('HOME')
    if home:
        filename=os.path.join(home,'.{}'.format(__config_filename))
        return check_cfg(filename)
    log.error('No HOME variable!')
    return None
@new_config_filename_getter
@logged
def get_git_cfg(log):
    git_dir=get_git_dir()
    if git_dir:
        filename=os.path.join(git_dir,__config_filename)
        return check_cfg(filename)
    return None

@logged
def get(log,key=None):
    if __config is None:
        parse()
    if key is None:
        return __config
    keys=key.split('.')
    val=__config.get(*keys,fallback=None)
    if val:
        log.info('{:} => {:}'.format(key,val))
        return val
    log.error('{:}:No such entry!'.format(key))
    return None

@logged
def parse(log):
    global __config
    __config=ConfigParser(interpolation=ExtendedInterpolation())
    log.debug('Created parser')
    for getter in __config_filename_getters:
        filename = getter()
        if filename:
            log.info('{:}:READING'.format(filename))
            __config.read(filename)
    s=StringIO('PARSED CONFIGURATION FILES\n')
    s.seek(0,2)
    __config.write(s)
    log.debug(s.getvalue())
# END config.py
