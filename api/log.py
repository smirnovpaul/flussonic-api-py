# -*- coding: utf-8 -*-
import logging

# Don`t forget in path: OS Windows '/'; OS Linux '\'
FORMAT = "%(asctime)s [%(levelname)s] [%(filename)s %(lineno)d] %(funcName)s: %(message)s"
FILE_NAME = "log/log.log"
LOGGER = logging.basicConfig(format=FORMAT, level=logging.DEBUG, filename=FILE_NAME)
