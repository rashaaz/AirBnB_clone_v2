#!/usr/bin/python3
'''Fabric script that creates and distributes an archive to your web servers
'''

import os
from datetime import datetime
from fabric.api import env, local, put, run, runs_once


env.hosts = ['54.86.220.207', '54.175.137.217']


@runs_once
def do_pack():
    """Generates a .tgz archive from the contents of the web_static folder"""
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    cur_time = datetime.now()
    ou = "versions/web_static_{}{}{}{}{}{}.tgz".format(
        cur_time.year,
        cur_time.month,
        cur_time.day,
        cur_time.hour,
        cur_time.minute,
        cur_time.second
    )
    try:
        print("Packing web_static to {}".format(ou))
        local("tar -cvzf {} web_static".format(ou))
        archize_size = os.stat(ou).st_size
        print("web_static packed: {} -> {} Bytes".format(ou, archize_size))
    except Exception:
        ou = None
    return ou


def do_deploy(archive_path):
    """Distributes an archive to your web servers
    """
    if not os.path.exists(archive_path):
        return False
    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = "/data/web_static/releases/{}/".format(folder_name)
    suc = False
    try:
        put(archive_path, "/tmp/{}".format(file_name))
        run("mkdir -p {}".format(folder_path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, folder_path))
        run("rm -rf /tmp/{}".format(file_name))
        run("mv {}web_static/* {}".format(folder_path, folder_path))
        run("rm -rf {}web_static".format(folder_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(folder_path))
        print('New version is now LIVE!')
        suc = True
    except Exception:
        suc = False
    return suc


def deploy():
    """Deploys the web static content
    """
    archive_path = do_pack()
    return do_deploy(archive_path) if archive_path else False
