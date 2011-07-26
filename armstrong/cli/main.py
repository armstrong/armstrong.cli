from __future__ import with_statement
import codecs
import glob
import os
import sys
import json
import re
import shutil

# TODO: use logging throughout for output

CWD = os.getcwd()


def init(*args):
    """Initial a new Armstrong project (armstrong init [path])"""
    # TODO: allow db to be configured from command line
    # TODO: interactive mode to ask questions for each variable
    from django.conf import settings

    # TODO: allow this path to be configured
    template_dir = os.path.realpath(os.path.join(
        os.path.dirname(__file__),
        "templates",
        "standard",
    ))

    settings.configure(DEBUG=False, TEMPLATE_DEBUG=False,
            TEMPLATE_DIRS=[template_dir, ])
    from django.template import Context, Template

    if len(args) > 0 and not args[-1][0] == '-':
        path = args[-1]
    else:
        path = CWD

    demo = '--demo' in args

    # TODO: allow this to be passed in via command line
    project_name = os.path.basename(path)

    context = Context({
        "project_name": project_name,
        "demo": demo
    })

    if not os.path.exists(path):
        os.mkdir(path)

    def source_files():
        for dirpath, dirnames, filenames in os.walk(template_dir):
            for dirname in dirnames:
                yield os.path.join(dirpath, dirname)
            for name in filenames:
                if not name.endswith(".pyc"):
                    yield os.path.join(dirpath, name)


    existing_files = []
    files = []
    for file in source_files():
        if file == "%s/__init__.py" % template_dir:
            # Don't need to create the project as a module
            continue

        if file.endswith("requirements/__init__.py"):
            # Ignore this file, it's just here so this gets picked up
            continue

        if not demo and '/_demo' in file:
            continue

        new_file = file.replace(template_dir, path)

        files.append((file, new_file))
        if os.path.exists(new_file):
            existing_files.append(new_file)

    if existing_files:
        output = [
                "Previous file detected!  Aborting!",
                "",
                "Please remove the following file if you wish to proceed:",
                "  %s\n" % ("\n  ".join(existing_files)),
        ]
        sys.stderr.write("\n".join(output))
        return -1

    template_paths = []
    with open(template_dir + '/manifest.json', 'r') as manifest_file:
        manifest = json.load(manifest_file)
        paths = manifest.get('templated', {}).get('include', [])
        template_paths = [re.compile(path) for path in paths]

    def path_matches(path):
        for expression in template_paths:
            if expression.match(path):
                return True
        return False

    for (source, dest) in files:
        if os.path.isdir(source):
            os.mkdir(dest)
        elif path_matches(os.path.relpath(source, template_dir)):
            with codecs.open(source, "r", "utf-8") as f:
                out = Template(f.read()).render(context)

            with codecs.open(dest, "w", "utf-8") as f:
                f.write(out)
        else:
            shutil.copy(source, dest)

    print "armstrong initialized!"


ARMSTRONG_COMMANDS = {
    "init": init
}


def usage():
    subcommands = []
    for name, subcommand in ARMSTRONG_COMMANDS.items():
        extra = ""
        if hasattr(subcommand, "__doc__") and subcommand.__doc__:
            extra = " - %s" % subcommand.__doc__
        subcommands.append("  %s%s" % (name, extra))
    subcommands = "  %s" % "\n  ".join(subcommands)

    help_msg = [
        "usage: armstrong <subcommand> <options>",
        "",
        "Available Subcommands:",
        subcommands,
    ]
    print "\n".join(help_msg)


def in_armstrong_project():
    return os.path.isdir(os.path.join(CWD, "config"))


def main():
    if len(sys.argv) < 2 and not in_armstrong_project():
        usage()
        sys.exit(0)

    if len(sys.argv) >= 2:
        subcommand = sys.argv[1]
        if subcommand in ARMSTRONG_COMMANDS:
            sys.exit(ARMSTRONG_COMMANDS[subcommand](*sys.argv[2:]))

    # are we in an armstrong project?
    if in_armstrong_project():
        # Make sure the current working dir is always in the path as the first
        # element.  Initial tests on a Homebrew Python installation result in
        # this not being the case.
        if CWD not in sys.path:
            sys.path.insert(0, CWD)

        settings_module = "config.development"
        if "--production" in sys.argv:
            settings_module = "config.production"
            del sys.argv[sys.argv["--production"]]

        try:
            __import__(settings_module, globals(), locals())
            settings = sys.modules[settings_module]
        except ImportError, e:
            sys.stderr.write("Unable to import %s: %s" % (settings_module, e))
            sys.exit(1)
        from django.core.management import execute_manager
        execute_manager(settings)
