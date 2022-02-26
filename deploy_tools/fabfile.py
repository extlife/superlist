from fabric import task
import random

REPO_URL = 'git@github.com:extlife/superlist.git'
PROJECT = 'superlist'

@task
def deploy(c):
    site_folder = f'/home/{c.user}/sites/{c.host}'
    source_folder = site_folder + '/source'

    create_directory_structure_if_necessary(c, site_folder)
    get_latest_source(c, source_folder)
    update_settings(c, source_folder)
    update_virtualenv(c, source_folder)
    update_static_files(c, source_folder)
    update_database(c, source_folder)

    configure_nginx(c, source_folder)
    configure_gunicorn(c, source_folder)

def append(c, fname, text):
        c.run(f'grep -qxF -- "{text}" "{fname}" || echo "{text}" >> "{fname}"')

def create_directory_structure_if_necessary(c, site_folder):
    for subfolder in ('database', 'static', 'venv', 'source'):
        c.run(f'mkdir -p {site_folder}/{subfolder}')

def get_latest_source(c, source_folder):
    if not c.run(f'test -d {source_folder}/.git', warn=True).failed:
        c.run(f'cd {source_folder} && git fetch')
    else:
        c.run(f'git clone {REPO_URL} {source_folder}')
    current_commit = c.local('git log -n 1 --format=%H', hide='stdout').stdout
    c.run(f'cd {source_folder} && git reset --hard {current_commit}', hide='stdout')

def update_settings(c, source_folder):
    settings_path = source_folder + f'/{PROJECT}/settings.py'
    c.run(f'sed -i -r "s/DEBUG = True/DEBUG = False/g" {settings_path}')
    c.run(f'sed -i -r "s/ALLOWED_HOSTS =.+$/ALLOWED_HOSTS = [\'{c.host}\']/g" {settings_path}')
    secret_key_file = source_folder + f'/{PROJECT}/secret_key.py'
    if c.run(f'test -f {secret_key_file}', warn=True).failed:
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        c.run(f'echo "SECRET_KEY = \'{key}\'" > {secret_key_file}')
    append(c, settings_path, 'from .secret_key import SECRET_KEY')

def update_virtualenv(c, source_folder):
    venv_folder = source_folder + '/../venv'
    if c.run(f'test -f {venv_folder}/bin/pip', warn=True).failed:
        c.run(f'python3.8 -m venv {venv_folder}')
    c.run(f'{venv_folder}/bin/pip install -r {source_folder}/requirements.txt')

def update_static_files(c, source_folder):
    c.run(f'cd {source_folder} && ../venv/bin/python manage.py collectstatic --no-input')

def update_database(c, source_folder):
    c.run(f'cd {source_folder} && ../venv/bin/python manage.py migrate --no-input')

def configure_nginx(c, source_folder):
    tools_folder = source_folder + '/deploy_tools'
    c.sudo(f'cp {tools_folder}/nginx.template.conf /etc/nginx/sites-available/{c.host}')
    c.sudo(f'sed -i "s/SITENAME/{c.host}/g;s/USER/{c.user}/g" /etc/nginx/sites-available/{c.host}')
    c.sudo(f'ln -s -f /etc/nginx/sites-available/{c.host} /etc/nginx/sites-enabled/{c.host}')
    c.sudo('systemctl reload nginx')

def configure_gunicorn(c, source_folder):
    tools_folder = source_folder + '/deploy_tools'
    c.sudo(f'cp {tools_folder}/gunicorn-systemd.template.service'
        + f' /etc/systemd/system/gunicorn-{c.host}.service')
    c.sudo(f'sed -i "s/SITENAME/{c.host}/g;s/USER/{c.user}/g;s/PROJECT/{PROJECT}/g"'
        + f' /etc/systemd/system/gunicorn-{c.host}.service')
    c.sudo('systemctl daemon-reload')
    c.sudo(f'systemctl enable gunicorn-{c.host}')
    c.sudo(f'systemctl start gunicorn-{c.host}')


# fab -H extlife@superlist-product.com --prompt-for-sudo-password deploy --echo 
