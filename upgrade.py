#!/var/venv/bin/python3.5

import pip
from subprocess import call


for dist in pip.get_installed_distributions():
    call("pip install --upgrade " + dist.project_name, shell=True)
