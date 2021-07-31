import os
import logging
import database

# create logger
log = logging.getLogger(__name__)


def get_monitored_folders():
    try:
        config = database.get_config()

        return config['monitored_folders']
    except Exception as e:
        log.fatal("Unable to load monitored folders config: %s", str(e))


def get_config_reload_interval():
    try:
        config = database.get_config()

        return config['config_reload_interval']
    except Exception as e:
        log.fatal("Unable to load config reload interval config: %s", str(e))


def get_folder_scan_interval():
    try:
        config = database.get_config()

        return config['scan_interval']
    except Exception as e:
        log.fatal("Unable to load folder scan interval config: %s", str(e))
