import logging
import solarcity_mqtt.parser
import os
import time

from ConfigParser import RawConfigParser
from watchdog.events import FileSystemEventHandler

kLog = logging.getLogger(__name__)


class SolarEventHandler(FileSystemEventHandler):
    def __init__(self,  config_path, callback):
        self.config = RawConfigParser()
        self.config.read(config_path)
        self.callback = callback

    def on_created(self, event):
        if (not event.is_directory and
            os.path.basename(event.src_path).startswith(
                self.config.get('data', 'source'))):
            kLog.info("%s created", event.src_path)
            # Wait 10 seconds to be sure tcpflow filled the message.
            time.sleep(10)
            values = solarcity_mqtt.parser.parser(event.src_path)
            kLog.debug("values")
            if values:
                self.callback(values)
        if self.config.getboolean('data', 'delete'):
            os.remove(event.src_path)
