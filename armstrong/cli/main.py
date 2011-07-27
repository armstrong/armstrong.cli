from __future__ import with_statement
import os
import sys
import argparse

from .commands.init import init
from .commands.import_wordpress import import_wordpress
from django.core.management import execute_manager, get_commands

# TODO: use logging throughout for output
CWD = os.getcwd()
ENTRY_POINT = 'armstrong.commands'

def in_armstrong_project():
    return os.path.isdir(os.path.join(CWD, "config"))

def main():
    parser = argparse.ArgumentParser(description='Choose subcommand to run.')
    subparsers = parser.add_subparsers(title='subcommands')

    from pkg_resources import iter_entry_points

    loaded = {}
    for ep in iter_entry_points(group=ENTRY_POINT):
        if ep.name in loaded:
            continue
        loaded[ep.name] = True
        command = ep.load()
        armstrong_parser = subparsers.add_parser(ep.name,
                description=command.__doc__,
                help=command.__doc__)
        if hasattr(command, 'build_parser'):
            command.build_parser(armstrong_parser)
        armstrong_parser.set_defaults(func=command)

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
    new_argv = sys.argv[0:2] + argv
    execute_manager(settings, argv=new_argv)
