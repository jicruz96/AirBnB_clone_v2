#!/usr/bin/python3
""" generates a .tgz archive of web_stack folder """

from datetime import datetime as time
from fabric.api import local


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
