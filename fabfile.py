import os
from fabric.api import run, env, cd, local

env.use_ssh_config = True
env.hosts = ['yj']


def host_type():
    run('uname -s')


APP_ROOT = "/data/apps/dash"


def root(x):
    return os.path.join(APP_ROOT, x)


VENV_ROOT = root(".venv")
PYTHON = root(".venv/bin/python")
PIP = root(".venv/bin/pip")
MANAGE = root("manage.py")


def migrate():
    run('{0} {1} migrate'.format(PYTHON, MANAGE))


def install_depends():
    run('{0} install - r . / requirements / prod.txt'.format(PIP))


def restart():
    run('pm2 restart dash')


def publish():
    local('git push yj')
    with cd(APP_ROOT):
        install_depends()
        migrate()
        restart()
        collect_static()


def collect_static():
    run('{0} {1} collectstatic -l --no-input'.format(PYTHON, MANAGE))


def reload():
    """reload services"""
