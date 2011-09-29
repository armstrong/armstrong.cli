import os


def command():
    # TODO: make this look for entry_points so third-party templates can be used
    # TODO: make this verify that there's a manifest.json present
    # TODO: make this display manifest.json's description along side template names
    import armstrong.cli.templates
    p = armstrong.cli.templates.__path__[0]
    templates = [a for a in os.listdir(p) if os.path.isdir(os.path.join(p, a))]
    print "The following templates are available:"
    print "\n    %s" % "\n    ".join(templates)
