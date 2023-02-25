import logging
import os
# 记录转发过的消息
from logging import handlers

IMAGE_PATH = f"{os.path.abspath(os.path.join(os.path.dirname(__file__)))}/"
if not os.path.exists(f"{IMAGE_PATH}/log/"):
    os.mkdir(f"{IMAGE_PATH}/log/")
IMAGE_PATH += "/log/"
file = f"{IMAGE_PATH}record.log"


class Log:
    def __init__(self):
        self.log = logging.getLogger('record')
        self.log.setLevel(logging.DEBUG)

    def get_formatter(self):
        return logging.Formatter('%(asctime)s --- %(levelname)s: [%(message)s]')

    def file_handler(self):
        file_handler = logging.FileHandler(file)
        file_handler.setLevel(level=logging.INFO)
        file_handler.setFormatter(self.get_formatter())
        return file_handler

    def time_rotating_file_handler(self):
        time_rotating_file_handler = handlers.TimedRotatingFileHandler(filename=file, when='D')
        time_rotating_file_handler.setLevel(logging.INFO)
        time_rotating_file_handler.setFormatter(self.get_formatter())
        return time_rotating_file_handler

    def get_log(self):
        self.log.addHandler(self.time_rotating_file_handler())
        return self.log


logger = Log().get_log()