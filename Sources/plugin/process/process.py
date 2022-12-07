import asyncio
import logging


class ProcessManager():

    def __init__(self, notifier, queue=asyncio.Queue()):
        self.queue = queue
        self.notifier = notifier

    async def enqueue(self, command):
        try:
            await self.queue.put(command)
        except Exception as err:
            logging.critical(err)

    async def process(self):
        while True:
            try:
                command = await self.queue.get()
                result = await command.execute()
                self.queue.task_done()
                logging.critical(r"OUTPUT: {}".format(result))
                if result:
                    output = result['output']
                    code = result['code']
                    self.notifier.notify(title="STREAMDECK PYTHON PLUGIN EXIT CODE: {}".format(
                        code), message="Received output of process:\n\n {}".format(output))
            except Exception as err:
                logging.critical(err)
