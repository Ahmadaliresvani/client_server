import logging
import os
import pytz
import datetime


# change time zone for logger
def timetz(*args):
    return datetime.datetime.now(pytz.timezone("EET")).timetuple()


def check_dir_exists(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)


def create_logger(name, dir_name):
    """this function create logger object and return it"""
    # first check dir exists or not
    check_dir_exists(dir_name)
    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # create handler and set level
    fh = logging.FileHandler(os.path.join(dir_name, name + ".log"), mode="w")
    fh.setLevel(logging.INFO)

    # create formatter
    logging.Formatter.converter = timetz
    formatter = logging.Formatter("%(asctime)s  %(message)s")

    # add formatter to fh
    fh.setFormatter(formatter)

    # add fh to logger
    logger.addHandler(fh)

    return logger
