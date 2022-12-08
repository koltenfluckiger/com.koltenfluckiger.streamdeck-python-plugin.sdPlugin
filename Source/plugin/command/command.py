import asyncio
import logging
import traceback

class Command:

    def __init__(self, command, return_flag):
        self.command = command
        self.return_flag = return_flag

    async def execute(self):
        try:
            DETACHED_PROCESS = 0x00000008
            process = await asyncio.create_subprocess_shell(r"{}".format(self.command), stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE, creationflags=DETACHED_PROCESS)
            stdout, stderr = await process.communicate()
            output = stdout.decode().strip()
            code = process.returncode
            logging.info("Output: {}".format(output))
            logging.info("Error Code: {}".format(code))
            if self.return_flag:
                return {"output": output, "code": code, "error": stderr.decode().strip()}
            else:
                return None
        except Exception as err:
            logging.critical("ERROR: {}".format(err))
            logging.critical(f"Traceback: {traceback.format_exc()}")
            
