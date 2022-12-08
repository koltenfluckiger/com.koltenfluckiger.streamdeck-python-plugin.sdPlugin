import asyncio
import logging
import traceback


class ProcessManager():

    def __init__(self, notifier, queue=asyncio.Queue()):
        self.queue = queue
        self.notifier = notifier

    async def enqueue(self, command):
        try:
            await self.queue.put(command)
        except Exception as err:
            logging.critical(err)
            logging.critical(f"Traceback: {traceback.format_exc()}")

    async def process(self):
        while True:
            try:
                command = await self.queue.get()
                result = await command.execute()
                self.queue.task_done()
                if result:
                    output = result['output'] if len(
                        result['output']) != 0 else None
                    output = output if output else result['error']
                    output = "No output" if output == '' else output
                    logging.debug(f"Output: {output}")
                    self.notifier.notify(
                        title="StreamDeck Python Plugin Output", message=f"{output}")
            except Exception as err:
                logging.critical(err)
                logging.critical(f"Traceback: {traceback.format_exc()}")
