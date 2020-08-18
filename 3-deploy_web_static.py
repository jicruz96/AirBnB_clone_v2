#!/usr/bin/python3
""" generates a .tgz archive of web_stack folder """

from fabric.api import local, run, put, env
from os.path import exists
from datetime import datetime as time


web_01 = '35.190.188.58'
web_02 = '52.23.162.134'
env.hosts = [web_01, web_02]


def do_pack():
    """ does pack """

    time_and_date = time.now().strftime("%Y%m%d%H%M%S")
    archive_name = "versions/web_static_{}.tgz".format(time_and_date)

    local("if [ ! -d versions ]; then mkdir versions; fi")

    try:
        local("tar -czvf {} web_static/".format(archive_name))
        return archive_name
    except:
        return None


def do_deploy(archive_path):
    """ does deploy """

    if archive_path is None or not exists(archive_path):
        return False

    # Create strings for archive name, link path, and target directory
    archive_name = archive_path.split('/')[-1]
    link_path = '/data/web_static/current'
    dir = '/data/web_static/releases/{}/'.format(archive_name.split('.')[0])

    try:
        # Transfer archive
        put(archive_path, '/tmp/')

        # Make directory
        run('mkdir -p {}'.format(dir))

        # Extract contents of archive
        run('tar -xzf /tmp/{} -C {}'.format(archive_name, dir))

        # Delete archive
        run('rm -rf /tmp/{}'.format(archive_name))

        # Move files from unzipped archive folder to dir
        run('mv {}web_static/* {}'.format(dir, dir))

        # Delete unzipped archive folder
        run('rm -rf {}web_static/'.format(dir))

        # Delete old symbolic link
        run('rm -rf {}'.format(link_path))

        # Make new symbolic link
        run('ln --symbolic {} {}'.format(dir, link_path))

        # If we made it here, print this message
        print('New version deployed!')

        return True
    except:
        return False


def deploy():
    """ deploys """
    return do_deploy(do_pack())
