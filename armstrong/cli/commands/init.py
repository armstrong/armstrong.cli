from __future__ import with_statement
import os
import sys
import re
import shutil
import codecs
import json
import argparse
from random import choice

CWD = os.getcwd()


class InitCommand(object):
    """Initialize a new Armstrong project"""

    def build_parser(self, parser):
        parser.description = \
                'Initialize a new Armstrong project from a template'
        parser.add_argument('--demo', action='store_true',
                help='install demo data and media assets')
        parser.add_argument('--template', default='standard',
                help='the project template to use')
        parser.add_argument('path', type=os.path.abspath, default='.',
                help='location to start a new Armstrong project')

    def __call__(self, template='standard', demo=False, path=CWD, **kwargs):
        # TODO: allow db to be configured from command line
        # TODO: interactive mode to ask questions for each variable
        from django.conf import settings

        # TODO: appropriate error output if non-existant template chosen
        template_dir = os.path.realpath(os.path.join(
            os.path.dirname(__file__),
            '..',
            "templates",
            template,
        ))

        settings.configure(DEBUG=False, TEMPLATE_DEBUG=False,
                TEMPLATE_DIRS=[template_dir, ])
        from django.template import Context, Template

        # TODO: allow this to be passed in via command line
        project_name = os.path.basename(path)

        # The secret key generate is borrowed directly from Django's startproject
        CHOICES = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        secret_key = ''.join([choice(CHOICES) for i in range(50)])
        context = Context({
            "project_name": project_name,
            "demo": demo,
            "secret_key": secret_key,
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
        excluded_files = [
                "%s/__init__.py" % template_dir,
                "%s/manifest.json" % template_dir,
        ]
        for file_name in source_files():
            if file_name in excluded_files:
                continue

            if file_name.endswith("requirements/__init__.py"):
                # Ignore this file, it's just here so this gets picked up
                continue

            new_file = file_name.replace(template_dir, path)

            files.append((file_name, new_file))
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

    @property
    def requires_armstrong(self):
        return False


init = InitCommand()
