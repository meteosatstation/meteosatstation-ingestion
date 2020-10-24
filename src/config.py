import os
import logging
import database

# create logger
log = logging.getLogger(__name__)


def get_monitored_folders():
    config = database.get_config()

    return config['monitored_folders']


def get_config_reload_interval():
    config = database.get_config()

    return config['config_reload_interval']


def get_folder_scan_interval():
    config = database.get_config()

    return config['scan_interval']