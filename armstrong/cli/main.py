import codecs
import glob
import os
import sys

# TODO: use logging throughout for output


def init():
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

    if len(sys.argv) > 2:
        path = sys.argv[2]
    else:
        path = os.getcwd()

    # TODO: allow this to be passed in via command line
    project_name = os.path.basename(path)

    context = Context({
        "project_name": project_name,
    })

    if not os.path.exists(path):
        os.mkdir(path)

    source_files = filter(
            lambda x: x.endswith(".pyc") is False,
            (glob.glob("%s/*" % template_dir) 
             + glob.glob("%s/*/*" % template_dir)))

    existing_files = []
    files = []
    for file in source_files:
        if file == "%s/__init__.py" % template_dir:
            # Don't need to create the project as a module
            continue

        if file.endswith("requirements/__init__.py"):
            # Ignore this file, it's just here so this gets picked up
            continue
        new_file = file.replace(template_dir, path)
        if file.endswith(".txt.py"):
            # Strip out the final .py -- it's there to make sure we know where
            # the file is included in a location alongside our project.
            new_file = new_file.replace(".py", "")

        files.append((file, new_file))
        if os.path.exists(new_file):
            existing_files.append(new_file)

    if existing_files:
        output = [
                "Previous file detected!  Aborting!",
                "",
                "Please remove the following file if you wish to proceed:",
                "  %s" % ("\n  ".join(existing_files)),
        ]
        sys.stderr.write("\n".join(output))
        return -1
    
    for (source, dest) in files:
        if os.path.isdir(source):
            os.mkdir(dest)
        else:
            # upgrade this to with statements as soon as 2.7 is ok as a dep
            f = codecs.open(source, "r", "utf-8")
            out = Template(f.read()).render(context)
            f.close()

            f = codecs.open(dest, "w", "utf-8")
            f.write(out)
            f.close()
    print "armstrong initialized!"



ARMSTRONG_COMMANDS = {
    "init": init
}


def usage():
    subcommands = "  %s" % ("\n  ".join(ARMSTRONG_COMMANDS.keys()))

    help_msg = [
        "usage: armstrong <subcommand> <options>",
        "",
        "Available Subcommands:",
        subcommands,
    ]
    print "\n".join(help_msg)


def main():
    if len(sys.argv) < 2:
        usage()
        sys.exit(0)

    subcommand = sys.argv[1]
    if subcommand in ARMSTRONG_COMMANDS:
        sys.exit(ARMSTRONG_COMMANDS[subcommand]())
