import asyncio
import os
import shutil
import subprocess
import time
from pySmartDL import SmartDL
from sample_config import Config
from telethon import events
from uniborg.util import admin_cmd, humanbytes, progress, time_formatter
import subprocess
import patoolib
from bin.cmrudl import *
from datetime import datetime
import io





@borg.on(admin_cmd(pattern=("cmrdl ?(.*)")))
async def _(event):
    url = event.pattern_match.group(1)
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    mone = await event.edit("Processing ...")
    # if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
    #     os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    # if event.reply_to_msg_id:
    start = datetime.now()
    reply_message = await event.get_reply_message()
    
    c_time = time.time()
    downloaded_file_name = Config.TMP_DOWNLOAD_DIRECTORY
    await event.edit("Finish downloading to my local")
    command_to_exec = f"./bin/cmrudl.py {url} -d ./DOWNLOADS/"
        # sp = subprocess.Popen(command_to_exec, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    reply_to_id = event.message.id
    PROCESS_RUN_TIME = 100
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    start_time = time.time() + PROCESS_RUN_TIME
    process = await asyncio.create_subprocess_shell(
    command_to_exec, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    logger.info(command_to_exec)
    OUTPUT = f"**Files in DOWNLOADS folder:**\n"
    stdout, stderr = await process.communicate()
    t_response = stdout.decode().strip()
    if len(stdout) > Config.MAX_MESSAGE_SIZE_LIMIT:
        with io.BytesIO(stdout) as out_file:
            out_file.name = "exec.txt"
            await borg.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=OUTPUT,
                reply_to=reply_to_id
            )
            # with open(str(out_file), encoding="utf-8") as file:
            #     x = [l.strip() for l in file]
            y = [x.rstrip() for x in open("exec.txt")]
            output_file_name = y[1]
            full_file_name = "./DOWNLOADS/" + output_file_name
            await borg.send_file(
                event.chat_id,
                full_file_name,
                force_document=True,
                allow_cache=False,
                caption=OUTPUT,
                reply_to=reply_to_id
            )
    if stderr.decode():
        await event.edit(f"**{stderr.decode()}**")
        return
    await event.edit(f"{OUTPUT}`{stdout.decode()}`")