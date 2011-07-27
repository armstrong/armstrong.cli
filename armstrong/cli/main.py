from __future__ import with_statement
import os
import sys
import argparse

from .commands.init import init
from .commands.import_wordpress import import_wordpress
from django.core.management import execute_manager, get_commands

# TODO: use logging throughout for output
CWD = os.getcwd()

def in_armstrong_project():
    return os.path.isdir(os.path.join(CWD, "config"))

def main():
    parser = argparse.ArgumentParser(description='Choose subcommand to run.',
            usage='armstrong subcommand [options]')
    subparsers = parser.add_subparsers(title='subcommands')

    init_parser = subparsers.add_parser('init', help='init --help')
    init_parser.add_argument('--demo', action='store_true',
            help='install demo data and media assets')
    init_parser.add_argument('--template', default='standard')
    init_parser.add_argument('path', type=os.path.abspath, default='.')
    init_parser.set_defaults(func=init)

    django_commands = get_commands().keys()
    django_commands.sort()
    for command in django_commands:
        dj_parser = subparsers.add_parser(command, help='')
        dj_parser.add_argument("--production", action='store_true')
        dj_parser.set_defaults(func=call_django)

    args, argv = parser.parse_known_args()
    kwargs = vars(args)
    func = kwargs.pop('func', None)
    if argv:
        func(argv=argv, **kwargs)
    else:
        func(**kwargs)

def call_django(argv=[], production=False):
    # Make sure the current working dir is always in the path as the first
    # element.  Initial tests on a Homebrew Python installation result in
    # this not being the case.
    if CWD not in sys.path:
        sys.path.insert(0, CWD)

    settings_module = "config.development"
    if production:
        settings_module = "config.production"

    try:
        __import__(settings_module, globals(), locals())
        settings = sys.modules[settings_module]
    except ImportError, e:
        sys.stderr.write("Unable to import %s: %s\n" % (settings_module, e))
        sys.exit(1)
    # django expects unparsed options, so we reset argv with the script name 
    # and subcommand
    passed_argv = sys.argv[0:2] + argv
    execute_manager(settings, argv=passed_argv)
