import asyncio
import logging
import platform


class Command:

    def __init__(self, command, return_flag):
        self.command = command
        self.return_flag = return_flag

    async def execute(self):
        try:
            kwargs = {}
            if 'windows' in platform.system().lower():
                DETACHED_PROCESS = 0x00000008
                kwargs['creationflags'] = DETACHED_PROCESS

            process = await asyncio.create_subprocess_shell(
                self.command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                **kwargs
            )
            stdout, stderr = await process.communicate()
            output = stdout.decode().strip()
            code = process.returncode
            logging.info(f"Output: {output}")
            logging.info(f"Error Code: {code}")
            if self.return_flag:
                return {"output": output, "code": code}
            else:
                return None
        except Exception as err:
            logging.critical(f"ERROR: {err}")
            return None
