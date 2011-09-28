from fabric.api import *


@task
def reinstall():
	local("pip uninstall -y `basename \`pwd\`` ; pip install .")