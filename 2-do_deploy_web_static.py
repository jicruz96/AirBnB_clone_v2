#!/usr/bin/python3
""" do_deploy baby """

from fabric.api import run, put, env
from os.path import exists

from fabric.state import commands

web_01 = '35.190.188.58'
web_02 = '52.23.162.134'
env.hosts = [web_01, web_02]


def do_deploy(archive_path):
    """ does deploy """

    if not exists(archive_path):
        return False

    archive_name = archive_path.split('/')[-1]
    link_path = '/data/web_static/current'
    put(archive_path, '/tmp')

    dir = '/data/web_static/releases/{}/'.format(archive_name.split('.')[0])
    mkdir = 'if [ ! -d {} ]; then mkdir -p {}; fi'.format(dir, dir),
    extract = 'tar -xzf /tmp/{} -C {}'.format(archive_name)
    mv_files = 'mv {}web_static/* {}'.format(dir, dir)
    rm_dir = 'rm -rf {}web_static/'.format(dir)
    rm_tgz = 'rm -rf /tmp/{}'.format(archive_name)
    rm_link = 'rm -rf {}'.format(link_path)
    ln = 'ln --symbolic {} {}'.format(dir, link_path)
    commands = [mkdir, extract, mv_files, rm_dir, rm_tgz, rm_link, ln]
    try:
        for command in commands:
            run(command)
        return True
    except:
        return False
