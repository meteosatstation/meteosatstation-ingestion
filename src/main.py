import os
import sys
import logging
import config
import time
import folder_scanner

# create logger
log = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


def run():
    log.info("Starting up")

    # get paths to scan
    scanning_paths = None
    scan_interval = None
    config_reload_interval = None

    config_reload_loop_count = 0

    while True:
        log.debug("Start main loop")
        log.debug("config_reload_loop_count is %s", str(config_reload_loop_count))

        # load initial config
        if config_reload_interval is None or config_reload_interval is config_reload_loop_count:
            log.info("Reloading config")
            config_reload_interval = config.get_config_reload_interval()
            config_reload_loop_count = 0

        if scanning_paths is None or config_reload_loop_count is 0:
            scanning_paths = config.get_monitored_folders()

        if scan_interval is None or config_reload_loop_count is 0:
            scan_interval = config.get_folder_scan_interval()

        # do the actual scanning
        for scanning_path in scanning_paths:
            log.info("Starting scan of %s", scanning_path['path'])
            folder_scanner.scan_folder(scanning_path)
            log.debug("Scan of %s completed", scanning_path['path'])

        # sleep for scan_interval
        time.sleep(scan_interval)

        config_reload_loop_count = config_reload_loop_count + 1
        log.debug("End main loop")


if __name__ == '__main__':
    run()

