"""Util functions used for the redis queue operations"""

import logging
import subprocess
from datetime import datetime
from flask import current_app as app

def restart_pi_process():
    """
    Reboot the pi using the redis queue worker.
    Returns:
         boolean True/False
    """
    cmd = "sudo reboot"
    try:
        proc = subprocess.Popen(
            "/bin/bash", shell=False, stdin=subprocess.PIPE,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        (stdout, stderr) = proc.communicate(cmd.encode("utf-8"))
        return True
    except Exception as e:
        app.logger.error(e)
        return False

def upgrade_pi_process():
    """
    Start a sub process to upgrade and reboot the pi.
    Logs the output to a log file in deployment/upgrade_logs

    Returns:
         boolean True/False
    """
    cmd = "./deployment/upgrade_pi.sh"
    proc = subprocess.Popen(
        "/bin/bash", shell=False, stdin=subprocess.PIPE,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    (stdout, stderr) = proc.communicate(cmd.encode("utf-8"))

    # Setup custom logger for upgrade
    timestamp = datetime.now().strftime('%Y_%m_%d')
    file = "./deployment/logs/{d}_upgrade.log".format(d=timestamp)
    upgrade_handler = logging.FileHandler(file)
    upgrade_logger = logging.getLogger("upgrade_logging")
    upgrade_logger.setLevel(logging.INFO)
    upgrade_logger.addHandler(upgrade_handler)

    upgrade_logger.info(stdout)
    upgrade_logger.error(stderr)

    return True