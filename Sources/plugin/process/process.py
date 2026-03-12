import asyncio
import logging


class ProcessManager():

    def __init__(self, notifier, queue=None):
        self.queue = queue if queue is not None else asyncio.Queue()
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
                logging.debug(f"OUTPUT: {result}")
                if result:
                    output = result['output']
                    code = result['code']
                    self.notifier.notify(
                        title=f"STREAMDECK PYTHON PLUGIN EXIT CODE: {code}",
                        message=f"Received output of process:\n\n {output}")
            except Exception as err:
                logging.critical(err)
