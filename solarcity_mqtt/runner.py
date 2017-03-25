import solarcity_mqtt.collector
import solarcity_mqtt.mqtt
import logging
import time
import argparse
from ConfigParser import RawConfigParser
from watchdog.observers import Observer

kAsyncLoopTimeout = 5

kLog = logging.getLogger(__name__)


class Runner(object):
    def __init__(self, config_path):
        self.config = RawConfigParser()
        self.config.read(config_path)
        self.observer = Observer()
        self.event_handler = solarcity_mqtt.collector.SolarEventHandler(
        config_path, self.recv_message)
        self.mqtt = solarcity_mqtt.mqtt.MosquittoClient(config_path)

    def start(self):
        path = self.config.get('data', 'path')
        self.observer.schedule(
        self.event_handler, path, recursive=False)
        self.mqtt.start()
        self.observer.start()
        self.observer.join()

    def stop(self):
        self.observer.stop()
        self.mqtt.stop()

    def recv_message(self, values):
        self.mqtt.publish(values)


def main():
    parser = argparse.ArgumentParser(
    description="""Listens on the serial port for power usage information,
    and relays it to an MQTT server""")
    parser.add_argument('config', help='Path to configuration file')
    args = parser.parse_args()
    config = RawConfigParser()
    config.read(args.config)
    log_level = config.get('logging', 'level')
    logging.basicConfig(level=getattr(logging, log_level))
    runner = Runner(args.config)
    runner.start()
    while True:
    try:
        time.sleep(5)
    except KeyboardInterrupt:
        break
    runner.stop()

if __name__ == '__main__':
    main()
