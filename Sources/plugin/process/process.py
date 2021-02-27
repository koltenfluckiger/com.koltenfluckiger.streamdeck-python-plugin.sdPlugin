import asyncio
import logging

class ProcessManager():

    def __init__(self):
        self.queue = asyncio.Queue()

    async def enqueue(self, command):
        try:
            await self.queue.put(command)
        except Exception as err:
            logging.critical(err)

    async def process(self):
        while not self.queue.empty():
            try:
                command = await self.queue.get()
                result = await command.execute()
                self.queue.task_done()
                return result
            except Exception as err:
                logging.critical(err)
