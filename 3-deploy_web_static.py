#!/usr/bin/python3
'''Fabric script that creates and distributes an archive to your web servers
'''

import os
from datetime import datetime
from fabric.api import env, local, put, run, runs_once


env.hosts = ['100.26.230.116', '18.233.65.185']


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
    fi_n = os.path.basename(archive_path)
    fol_n = fi_n.replace(".tgz", "")
    fol_p = "/data/web_static/releases/{}/".format(fol_n)
    suc = False
    try:
        put(archive_path, "/tmp/{}".format(fi_n))
        run("mkdir -p {}".format(fol_p))
        run("tar -xzf /tmp/{} -C {}".format(fi_n, fol_p))
        run("rm -rf /tmp/{}".format(fi_n))
        run("mv {}web_static/* {}".format(fol_p, fol_p))
        run("rm -rf {}web_static".format(fol_p))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(fol_p))
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
