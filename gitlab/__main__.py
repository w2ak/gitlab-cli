from . import logging,cli

# BEGIN __main__.py
logging.basicConfig(level=logging.WARNING)
# logging.getLogger('gitlab').setLevel(logging.DEBUG)
# logging.getLogger('gitlab.config').setLevel(logging.DEBUG)
logging.getLogger('gitlab.api').setLevel(logging.DEBUG)
logging.getLogger('gitlab.cli').setLevel(logging.DEBUG)

cli.run()
# END __main__.py
