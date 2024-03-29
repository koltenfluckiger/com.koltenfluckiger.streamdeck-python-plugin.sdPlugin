import sys
import asyncio
import logging
import re
import json
import websockets
import os
import pathlib
import traceback
from logging.handlers import RotatingFileHandler

from process import ProcessManager
from operatingsystem import OSManager
from cache import CacheManager
from notifier import Notifier
from command import Command


logging.basicConfig(
    handlers=[RotatingFileHandler(
        f'{pathlib.Path(os.environ["TEMP"]).joinpath("debug.log").resolve()}', maxBytes=100000, backupCount=10)],
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt='%Y-%m-%dT%H:%M:%S')


class Plugin(object):

    def __init__(self, port, pluginUUID, registerEvent, info, loop, process_manager, os_manager, cache_manager=CacheManager()):
        self.port = port
        self.pluginUUID = pluginUUID
        self.registerEvent = registerEvent
        self.info = info
        self.loop = loop
        self.process_manager = process_manager
        self.cache_manager = cache_manager
        self.os_manager = os_manager

    def __del__(self):
        try:
            self.websocket.close()
            self.loop.close()
        except Exception as err:
            logging.critical(err)
            logging.critical(f"Traceback: {traceback.format_exc()}")

    async def listen(self):
        try:
            await self._init_websocket()
            await self._register_websocket()
            await self.on_message()
        except Exception as err:
            logging.critical(err)
            logging.critical(f"Traceback: {traceback.format_exc()}")

    async def _init_websocket(self):
        uri = "ws://localhost:{}".format(self.port)
        try:
            self.websocket = await websockets.connect(uri)
            return
        except Exception as err:
            logging.critical(err)
            logging.critical(f"Traceback: {traceback.format_exc()}")

    async def _register_websocket(self):
        try:
            data = {
                "event": self.registerEvent,
                "uuid": self.pluginUUID
            }

            logging.info("Registering websocket...")
            await self.websocket.send(json.dumps(data))
            return
        except Exception as err:
            logging.critical(err)
            logging.critical(f"Traceback: {traceback.format_exc()}")

    async def on_message(self):
        try:
            async for message in self.websocket:
                await self.process_data(json.loads(message))
        except Exception as err:
            logging.critical(err)
            logging.critical(f"Traceback: {traceback.format_exc()}")

    async def send_message(self, event):
        try:
            logging.info("Sending event: {}".format(event))
            await self.websocket.send(event)
        except Exception as err:
            logging.critical(err)
            logging.critical(f"Traceback: {traceback.format_exc()}")

    def generate_command(self, data):
        try:
            file_location = data['settings']['filelocation']
            arguments = data['settings']['arguments']
            return_flag = data['settings']['returnflag']
            command = self.os_manager.generate_exec_path(
                file_location, arguments)
            new_command = Command(command, return_flag)
            logging.critical("Generating Command: {}".format(command))
            return new_command
        except Exception as err:
            logging.critical(err)
            logging.critical(f"Traceback: {traceback.format_exc()}")

    async def process_data(self, data):
        logging.info("Processing data: {}".format(data))
        try:
            if 'payload' in data:

                action = data['action']
                context = data['context']
                event = data['event']
                payload = data['payload']

                if event == 'keyDown':
                    command = self.generate_command(payload)
                    await self.process_manager.enqueue(command)
                    return

        except Exception as err:
            logging.critical(err)
            logging.critical(f"Traceback: {traceback.format_exc()}")


def parse_args(sys_args):
    args_length = len(sys_args)
    args = {}
    if args_length > 1:
        try:
            reg = re.compile('-(.*)')
            for i in range(1, args_length, 2):
                x = i
                y = i + 1
                flag = reg.search(sys.argv[x]).group(1)
                value = sys.argv[y]
                args[flag] = value
                logging.info("Flag: {}, Value: {}".format(flag, value))
        except Exception as err:
            logging.critical(err)
            logging.critical(f"Traceback: {traceback.format_exc()}")
    return args


def main():
    try:
        args = parse_args(sys.argv)
        logging.info(args)
        loop = asyncio.new_event_loop()
        eloop = asyncio.get_event_loop()
        os_manager = OSManager()
        os_type = os_manager._get_current_os()
        notifier = Notifier(os_type)
        process_manager = ProcessManager(notifier)

        plugin = Plugin(port=args['port'], pluginUUID=args['pluginUUID'],
                        registerEvent=args['registerEvent'], info=args['info'], loop=eloop, process_manager=process_manager, os_manager=os_manager)

        eloop.run_until_complete(asyncio.gather(
            plugin.listen(), process_manager.process()))
        eloop.run_forever()
        eloop.stop()
        eloop.close()
    except Exception as err:
        logging.critical(err)
        logging.critical(f"Traceback: {traceback.format_exc()}")
        eloop.stop()
        eloop.close()


if __name__ == '__main__':
    main()
