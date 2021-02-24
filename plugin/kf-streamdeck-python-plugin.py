import sys
import asyncio
import logging
import re
import json
import websockets

from process import ProcessManager
from operatingsystem import OSManager
from cache import CacheManager
from notifier import Notifier
from command import Command

logging.basicConfig(filename="debug.log", level=logging.CRITICAL)


class Plugin(object):

    def __init__(self, port, pluginUUID, registerEvent, info, loop):
        self.port = port
        self.pluginUUID = pluginUUID
        self.registerEvent = registerEvent
        self.info = info
        self.loop = loop
        self.process_manager = ProcessManager()
        self.cache_manager = CacheManager()
        self.os_manager = OSManager()
        self.notifier = Notifier(self.os_manager._get_current_os())

    def __del__(self):
        try:
            self.websocket.close()
            self.loop.close()
        except Exception as err:
            print(err)

    async def listen(self):
        try:
            await self._init_websocket()
            await self._register_websocket()
            await self.on_message()
        except Exception as err:
            print(err)
            logging.critical(err)

    async def _init_websocket(self):
        uri = "ws://localhost:{}".format(self.port)
        try:
            self.websocket = await websockets.client.connect(uri)
            return
        except Exception as err:
            logging.critical(err)

    async def _register_websocket(self):
        try:
            data = {
                "event": self.registerEvent,
                "uuid": self.pluginUUID
            }
            settings = {
                'event': 'getGlobalSettings',
                'context': self.pluginUUID
            }

            logging.critical("Registering websocket")
            await self.websocket.send(json.dumps(data))
            await self.websocket.send(json.dumps(settings))
            return
        except Exception as err:
            logging.critical(err)

    async def on_message(self):
        try:
            async for message in self.websocket:
                await self.process_data(json.loads(message))
        except Exception as err:
            logging.critical(err)

    async def send_message(self, event):
        try:
            logging.critical("Sending event {}".format(event))
            await self.websocket.send(event)
        except Exception as err:
            logging.critical(err)

    async def process_result(self, result):
        try:
            if result:
                output = result['output']
                code = result['code']
                self.notifier.notify(title="STREAMDECK PYTHON PLUGIN EXIT CODE: {}".format(
                    code), message="Received output of process:\n\n {}".format(output))
                return
            else:
                return
        except Exception as err:
            logging.critical(err)

    def generate_command(self, data):
        try:
            file_location = data['settings']['filelocation']
            arguments = data['settings']['arguments']
            return_flag = data['settings']['returnflag']
            command = self.os_manager.generate_exec_path(
                file_location, arguments)
            c = Command(command, return_flag)
            return c
        except Exception as err:
            logging.critical(err)

    async def process_data(self, data):
        logging.critical("Processing data: {}".format(data))
        try:
            if 'payload' in data:

                action = data['action']
                context = data['context']
                event = data['event']
                payload = data['payload']

                if event == 'keyDown':
                    command = self.generate_command(payload)
                    logging.critical(command.execute)
                    logging.critical(command.command)
                    await self.process_manager.enqueue(command)
                    result = await self.process_manager.process()
                    await self.process_result(result)
                    return

        except Exception as err:
            logging.critical(err)


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
                logging.critical("Flag: {}, Value: {}".format(flag, value))
        except Exception as err:
            logging.critical(err)
    return args


def main():
    try:
        args = parse_args(sys.argv)
        loop = asyncio.get_event_loop()
        plugin = Plugin(port=args['port'], pluginUUID=args['pluginUUID'],
                        registerEvent=args['registerEvent'], info=args['info'], loop=loop)
        loop.run_until_complete(plugin.listen())
        loop.run_forever()
    except Exception as err:
        logging.critical(err)


if __name__ == '__main__':
    main()
