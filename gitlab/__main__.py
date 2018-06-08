from . import parse_args,main,logging

# BEGIN __main__.py
logging.basicConfig(level=logging.INFO)
# logging.getLogger('gitlab').setLevel(logging.DEBUG)
# logging.getLogger('gitlab.config').setLevel(logging.DEBUG)
logging.getLogger('gitlab.api').setLevel(logging.DEBUG)

args = parse_args()
main(args)
# END __main__.py
