from subprocess import run
from pip._internal.utils.misc import get_installed_distributions


for dist in get_installed_distributions():
    run("pip install --upgrade " + dist.project_name, shell=True)
