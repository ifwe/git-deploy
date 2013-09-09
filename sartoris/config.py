"""
Config file for Sartoris.
"""

__authors__ = {
    'Ryan Faulkner': 'bobs.ur.uncle@gmail.com',
    'Patrick Reilly': 'patrick.reilly@gmail.com',
    'Ryan Lane': 'rlane@wikimedia.org',
}
__date__ = '2013-09-08'

from dulwich.config import StackedConfig
import subprocess
import sys
import logging

# Native git call
GIT_CALL = '/usr/bin/git'

# Codes emitted on exit conditions
exit_codes = {
    1: 'Operation failed.  Exiting.',
    2: 'A deployment has already been started.  Exiting.',
    3: 'Please enter valid arguments.  Exiting.',
    4: 'Missing lock file.  Exiting.',
    5: 'Could not reset.  Exiting.',
    6: 'Diff failed.  Exiting.',
    7: 'Missing tag(s).  Exiting.',
    8: 'Could not find last deploy tag.  Exiting.',
    9: 'Could not get listing from deploy target.  Exiting.',
    10: 'Please specify number of deploy tags to emit with -c.  Exiting',
    11: 'Could not find any deploys.  Exiting',
    12: 'Tagging failed. Exiting',
    20: 'Cannot find top level directory for the git repository. Exiting.',
    21: 'Missing system configuration item "hook-dir". Exiting.',
    22: 'Missing repo configuration item "tag-prefix". '
        'Please configure this using:'
        '\n\tgit config tag-prefix <repo>',
    23: 'Missing system configuration item "path". Exiting.',
    24: 'Missing system configuration item "user". Exiting.',
    25: 'Missing system configuration item "target". Exiting.',
    26: 'Missing system configuration item "remote". Exiting.',
    27: 'Missing system configuration item "branch". Exiting.',
    28: 'Missing system configuration item "user.name". Exiting.',
    29: 'Missing system configuration item "user.email". Exiting.',
    30: 'No deploy started. Please run: git deploy start',
    31: 'Failed to write tag on sync. Exiting.',
    32: 'Failed to write the .deploy file. Exiting.',
    40: 'Failed to run sync script. Exiting.',
    50: 'Failed to read the .deploy file. Exiting.',
}


# NullHandler was added in Python 3.1.
try:
    NullHandler = logging.NullHandler
except AttributeError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

# Add a do-nothing NullHandler to the module logger to prevent "No handlers
# could be found" errors. The calling code can still add other, more useful
# handlers, or otherwise configure logging.
log = logging.getLogger(__name__)
log.addHandler(NullHandler())


def set_log(args, out, err):
    """
    Sets the logger.

    Parameters:

        args    - command line args
        out     - stdout
        err     - stderr
    """
    level = logging.WARNING - ((args.verbose - args.quiet) * 10)
    if args.silent:
        level = logging.CRITICAL + 1

    log_format = "%(asctime)s %(levelname)-8s %(message)s"
    handler = logging.StreamHandler(err)
    handler.setFormatter(logging.Formatter(fmt=log_format,
                         datefmt='%b-%d %H:%M:%S'))
    log.addHandler(handler)
    log.setLevel(level)


def configure():
    """ Parse configuration from git config """
    sc = StackedConfig(StackedConfig.default_backends())
    config = {}

    # Get top level directory of project
    proc = subprocess.Popen(['git', 'rev-parse', '--show-toplevel'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    config['top_dir'] = proc.communicate()[0].strip()

    if proc.returncode != 0:
        exit_code = 20
        log.error("{0} :: {1}".format(__name__, exit_codes[exit_code]))
        sys.exit(exit_code)

    config['deploy_file'] = config['top_dir'] + '/.git/.deploy'

    # Define the key names, git config names, and error codes
    config_elements = {
        'hook_dir': ('deploy', 'hook-dir', 21),
        'path': ('deploy', 'path', 23),
        'user': ('deploy', 'user', 24),
        'target': ('deploy', 'target', 25),
        'repo_name': ('deploy', 'tag-prefix', 22),
        'remote': ('deploy', 'remote', 26),
        'branch': ('deploy', 'branch', 27),
        'user.name': ('user', 'name', 28),
        'user.email': ('user', 'email', 29),
    }

    # Assign the values of each git config element
    for key, value in config_elements.iteritems():
        try:
            config[key] = sc.get(value[0], value[1])
        except KeyError:
            exit_code = value[2]
            log.error("{0} :: {1}".format(__name__, exit_codes[exit_code]))
            sys.exit(exit_code)

    config['sync_dir'] = '{0}/sync'.format(config['hook_dir'])

    return config