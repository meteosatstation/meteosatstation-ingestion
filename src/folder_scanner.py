import logging
import os
import re
import database

# create logger
log = logging.getLogger(__name__)


def scan_folder(config):
    # you can specify a regex in the configuration and we'll only load in if it matches that
    if 'regex' in config:
        regex = re.compile(config['regex'])

    try:
        # get all files in the folder
        folder_listing = os.listdir(config['path'])

        for file in folder_listing:
            full_path = os.path.join(config['path'], file)

            # if we have regex matching enabled
            if 'regex' in config:
                if regex.match(file):
                    # load in the file
                    log.info("Loading in file %s because it matches our regex",
                             file)
                    database.load_file(full_path, config)

                    if config['delete_after_rx']:
                        log.info("Deleting file %s from received folder", file)
                        os.remove(full_path)

            # if we dont have regex matching enabled
            else:
                log.info("Loading in file %s", file)
                database.load_file(full_path, config)

                if config['delete_after_rx']:
                    log.info("Deleting file %s from received folder", file)
                    os.remove(full_path)
    except FileNotFoundError as e:
        log.error("Scanning directory not found: %s", str(e))
    except Exception as e:
        log.error("Unable to scan directory %s: %s", config['path'], str(e))
