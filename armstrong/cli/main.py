import os
import sys
import argparse

from .commands.init import init

# TODO: use logging throughout for output
ENTRY_POINT = 'armstrong.commands'
CONFIGURATION_MODULE = "settings"


def in_armstrong_project(some_path=None):
    if some_path is None:
        some_path = CWD
    joined = os.path.join(some_path, CONFIGURATION_MODULE)
    return os.path.isdir(joined) and \
                os.path.exists(os.path.join(joined, '__init__.py'))


def find_project_dir(path=os.getcwd()):
    """Attempt to find the project root, returns None if not found"""
    path_split = os.path.split(path)
    while path_split[1]:
        if in_armstrong_project(path):
            return path
        path = path_split[0]
        path_split = os.path.split(path)
    # we ran out of parents
    return None

CWD = find_project_dir() or os.getcwd()


def get_current_configuration():
    """Return appropriate settings name"""
    type = "production" if "--production" in sys.argv else "development"
    return "%s.%s" % (CONFIGURATION_MODULE, type)


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
        if (not in_armstrong_project() and
                getattr(command, "requires_armstrong", False)):
            continue
        armstrong_parser = subparsers.add_parser(ep.name,
                description=command.__doc__,
                help=command.__doc__)
        if hasattr(command, 'build_parser'):
            command.build_parser(armstrong_parser)
        armstrong_parser.set_defaults(func=command)

    if in_armstrong_project():
        # Make sure the current working dir is always in the path as the first
        # element.  Initial tests on a Homebrew Python installation result in
        # this not being the case.
        if CWD not in sys.path:
            sys.path.insert(0, CWD)

        try:
            settings_module = get_current_configuration()
            __import__(settings_module, globals(), locals())
            from django.core.management import setup_environ
            setup_environ(sys.modules[settings_module])
        except ImportError, e:
            sys.stderr.write("Unable to import %s: %s\n" %
                             (settings_module, e))
            sys.exit(1)
        from django.core.management import get_commands
        django_commands = get_commands().keys()
        django_commands.sort()
        for command in django_commands:
            dj_parser = subparsers.add_parser(command, help='')
            dj_parser.add_argument("--production", action='store_true',
                help='use %s.production setting' % CONFIGURATION_MODULE)
            dj_parser.set_defaults(func=call_django)

    args, argv = parser.parse_known_args()
    kwargs = vars(args)
    func = kwargs.pop('func', None)
    if argv:
        func(argv=argv, **kwargs)
    else:
        func(**kwargs)


def call_django(argv=[], production=False):
    if CWD not in sys.path:
        sys.path.insert(0, CWD)
    settings_module = "%s.development" % CONFIGURATION_MODULE
    if production:
        settings_module = "%s.production" % CONFIGURATION_MODULE
    settings = None
    try:
        __import__(settings_module, globals(), locals())
        settings = sys.modules[settings_module]
    except ImportError, e:
        sys.stderr.write("Unable to import %s: %s\n" % (settings_module, e))
        sys.exit(1)
    # django expects unparsed options, so we reset argv with the script name
    # and subcommand
    new_argv = sys.argv[0:2] + argv
    from django.core.management import execute_manager
    execute_manager(settings, argv=new_argv)
