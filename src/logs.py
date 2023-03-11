import logging


# basic logging settings
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


c_handler = logging.StreamHandler()
f_handler = logging.FileHandler("logs/logs.log", mode="w")

c_handler.setFormatter(logging.Formatter(
    "module: %(module)s - filename: %(filename)s - %(levelname)s - %(message)s"))
f_handler.setFormatter(logging.Formatter(
    "%(asctime)s - %(filename)s - %(module)s - %(levelname)s - %(message)s"))

f_handler.setLevel(logging.WARNING)

logger.addHandler(c_handler)
logger.addHandler(f_handler)
