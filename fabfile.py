# This Python file uses the following encoding: utf-8
# Original code from: Test-Driven Development with Python by Harry Percival (O’Reilly).
# Copyright 2014 Harry Percival, 978-1-449-36482-3.”

from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://bitbucket.org/openrem/openrem.git'

def deploy():
    site_folder = '/home/{0}/sites/{1}'.format(env.user, env.host)
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    # _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
    _restart_gunicorn()


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run('mkdir -p {0}/{1}'.format(site_folder, subfolder))


def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run('cd {0} && git fetch'.format(source_folder))
    else:
        run('git clone {0} {1}'.format(REPO_URL, source_folder))
    # current_commit = local("git log -n 1 --format=%H", capture=True)
    current_commit = local("echo $BITBUCKET_COMMIT", capture=True)
    run('cd {0} && git reset --hard {1}'.format(source_folder, current_commit))


def _update_settings(source_folder, site_name):
    settings_path = source_folder + '/openrem/openremproject/local_settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        'ALLOWED_HOSTS = ["{0}"]'.format(site_name)
    )
    secret_key_file = source_folder + '/openrem/openremproject/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, 'SECRET_KEY = "{0}"'.format(key))
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def _update_virtualenv(source_folder):
    virtualenv_folder = source_folder + '/../virtualenv'
    # if not exists(virtualenv_folder + '/bin/pip'):
    #     run('virtualenv {0}'.format(virtualenv_folder))
    # run('{0}/bin/pip install -r {1}/requirements.txt'.format(virtualenv_folder, source_folder))
    run('{0}/bin/pip install -e {1}/'.format(virtualenv_folder, source_folder))


def _update_static_files(source_folder):
    run(
        'cd {0}'
        ' && ../virtualenv/bin/python openrem/manage.py collectstatic --noinput'.format(source_folder)
    )


def _update_database(source_folder):
    run(
        'cd {0}'
        ' && ../virtualenv/bin/python openrem/manage.py makemigrations remapp --noinput'.format(source_folder)
    )
    run(
        'cd {0}'
        ' && ../virtualenv/bin/python openrem/manage.py migrate --noinput'.format(source_folder)
    )


def _restart_gunicorn():
    run(
        'sudo /usr/sbin/service gunicorn-{0} restart'.format(env.host)
    )