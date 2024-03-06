#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""
from fabric.api import *
from datetime import datetime
from os import path


env.hosts = ['100.26.230.116', '18.233.65.185']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_deploy(archive_path):
    """Distributes an archive to your web servers
    """
    try:
        if not (path.exists(archive_path)):
            return False

            # upload archive
            put(archive_path, '/tmp/')

            # create target dir
            tp = archive_path[-18:-4]
            run('sudo mkdir -p /data/web_static/\
releases/web_static_{}/'.format(tp))

            # uncompress archive and delete .tgz
            run('sudo tar -xzf /tmp/web_static_{}.tgz -C \
/data/web_static/releases/web_static_{}/'
                .format(tp, tp))

            # remove archive
            run('sudo rm /tmp/web_static_{}.tgz'.format(tp))

            # move contents into host web_static
            run('sudo mv /data/web_static/releases/web_static_{}/web_static/* \
/data/web_static/releases/web_static_{}/'.format(tp, tp))

            # remove extraneous web_static dir
            run('sudo rm -rf /data/web_static/releases/\
web_static_{}/web_static'
                .format(tp))

            # delete pre-existing sym link
            run('sudo rm -rf /data/web_static/current')

            # re-establish symbolic link
            run('sudo ln -s /data/web_static/releases/\
web_static_{}/ /data/web_static/current'.format(tp))
        except:
            return False

        # return True on success
        return True
