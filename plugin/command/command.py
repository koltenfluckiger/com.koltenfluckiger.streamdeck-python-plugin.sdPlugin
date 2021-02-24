import asyncio
import logging


class Command:

    def __init__(self, command, return_flag):
        self.command = command
        self.return_flag = return_flag
    
    async def execute(self):
        try:
            process = await asyncio.create_subprocess_shell(self.command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
            stdout, stderr = await process.communicate()
            output = stdout.decode().strip()
            code = process.returncode
            if self.return_flag:
                return {"output": output, "code": code}
            else:
                return None
        except Exception as err:
            logging.critical(err)
