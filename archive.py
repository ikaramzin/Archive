#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import timedelta
from ENV import *            # Импортируются переменные
import logging
import os
import os.path
import shutil
import time

file_name = archive_1day + archive_name + '-' + time.strftime("%Y%m%d")


def func_birthday(file):
    return os.stat(file).st_mtime


def func_num_of_files(max_num, directory):
    cur_num = len([name for name in os.listdir(directory)
                   if os.path.isfile(os.path.join(directory, name))])
    if cur_num > max_num:
        return True
    else:
        return False


def date_of_file(directory, old=False):
    files = os.listdir(directory)
    files = [os.path.join(directory, file) for file in files]
    files = [file for file in files if os.path.isfile(file)]
    if old:
        value = min(files, key=func_birthday)
    else:
        value = max(files, key=func_birthday)
    return value, func_birthday(value)


if __name__ == '__main__':
    logging.basicConfig(
        filename='archive.log',
        level=logging.DEBUG,
        format='{asctime} {name} {levelname} {message}',
        datefmt='%Y-%m-%d %H:%M:%S',
        style='{'
    )

    cur_time = time.time()
    last_in_1day, f_time = date_of_file(archive_1day)
    logging.debug(f'cur_time = {time.ctime(cur_time)}')
    logging.debug(f'f_time = {time.ctime(f_time)}')
    period = timedelta(seconds=cur_time - f_time)
    logging.debug(f'days = {period.days}')
    if period.days > 0:
        shutil.make_archive(file_name, archive_format, archive_target)
        logging.debug(f'{file_name=} is created')
    else:
        logging.debug(f'file {last_in_1day} is actual')
        exit('\narchive finish\n')


    if func_num_of_files(3, archive_1day):
        first_in_1day, f_time = date_of_file(archive_1day, old=True)
        logging.debug(f'{first_in_1day=}')
        logging.debug(f'time={time.ctime(f_time)}')
        last_in_3day, l_time = date_of_file(archive_3day)
        logging.debug(f'{last_in_3day=}')
        logging.debug(f'time={time.ctime(l_time)}')
        period = timedelta(seconds=f_time-l_time)
        logging.debug(f'days = {period.days}')
        if period.days > 3:
            shutil.move(first_in_1day, archive_3day)
            logging.debug(f'file {first_in_1day} is moved')
        else:
            os.remove(first_in_1day)
            logging.debug(f'file {first_in_1day} is removed')
            exit('\narchive finish\n')
    else:
        exit('\narchive finish\n')


    if func_num_of_files(3, archive_3day):
        first_in_3day, f_time = date_of_file(archive_3day, old=True)
        logging.debug(f'{first_in_3day=}')
        logging.debug(f'time={time.ctime(f_time)}')
        last_in_week, l_time = date_of_file(archive_1week)
        logging.debug(f'{last_in_week=}')
        logging.debug(f'time={time.ctime(l_time)}')
        period = timedelta(seconds=f_time-l_time)
        logging.debug(f'days = {period.days}')
        if period.days > 7:
            shutil.move(first_in_3day, archive_1week)
            logging.debug(f'file {first_in_3day} is moved')
        else:
            os.remove(first_in_3day)
            logging.debug(f'file {first_in_3day} is removed')
            exit('\narchive finish\n')
    else:
        exit('\narchive finish\n')

    if func_num_of_files(3, archive_1week):
        first_in_week, f_time = date_of_file(archive_1week, old=True)
        logging.debug(f'{first_in_week=}')
        logging.debug(f'time={time.ctime(f_time)}')
        last_in_1month, l_time = date_of_file(archive_1month)
        logging.debug(f'{last_in_1month=}')
        logging.debug(f'time={time.ctime(l_time)}')
        period = timedelta(seconds=f_time-l_time)
        logging.debug(f'days = {period.days}')
        if period.days > 30:
            shutil.move(first_in_week, archive_1month)
            logging.debug(f'file {first_in_week} is moved')
        else:
            os.remove(first_in_week)
            logging.debug(f'file {first_in_week} is removed')
            exit('\narchive finish\n')
    else:
        exit('\narchive finish\n')

    if func_num_of_files(3, archive_1month):
        first_in_1month, f_time = date_of_file(archive_1month, old=True)
        logging.debug(f'{first_in_1month=}')
        logging.debug(f'time={time.ctime(f_time)}')
        last_in_3month, l_time = date_of_file(archive_3month)
        logging.debug(f'{last_in_3month=}')
        logging.debug(f'time={time.ctime(l_time)}')
        period = timedelta(seconds=f_time - l_time)
        logging.debug(f'days = {period.days}')
        if period.days > 30*3:
            shutil.move(first_in_1month, archive_3month)
            logging.debug(f'file {first_in_1month} is moved')
        else:
            os.remove(first_in_1month)
            logging.debug(f'file {first_in_1month} is removed')
            exit('\narchive finish\n')
    else:
        exit('\narchive finish\n')

    if func_num_of_files(3, archive_3month):
        first_in_3month, f_time = date_of_file(archive_3month, old=True)
        logging.debug(f'{first_in_3month=}')
        logging.debug(f'time={time.ctime(f_time)}')
        last_in_6month, l_time = date_of_file(archive_6month)
        logging.debug(f'{last_in_6month=}')
        logging.debug(f'time={time.ctime(l_time)}')
        period = timedelta(seconds=f_time - l_time)
        logging.debug(f'days = {period.days}')
        if period.days > 30*6:
            shutil.move(first_in_3month, archive_6month)
            logging.debug(f'file {first_in_3month} is moved')
        else:
            os.remove(first_in_3month)
            logging.debug(f'file {first_in_3month} is removed')
            exit('\narchive finish\n')
    else:
        exit('\narchive finish\n')

    if func_num_of_files(3, archive_6month):
        first_in_6month, f_time = date_of_file(archive_6month, old=True)
        logging.debug(f'{first_in_6month=}')
        logging.debug(f'time={time.ctime(f_time)}')
        os.remove(first_in_6month)
        logging.debug(f'file {first_in_6month} is removed')
        exit('\narchive finish\n')
    else:
        exit('\narchive finish\n')
