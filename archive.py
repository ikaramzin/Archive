#!/usr/bin/python3
# -*- coding: utf-8 -*-

from ENV import *
from datetime import timedelta
import logging
import os
import os.path
import shutil
import time
import hashlib

file_name = archive_1day + archive_name + '-' + time.strftime("%Y%m%d")


def func_birthday(file):
    """
    определяет дату создания файла
    :param file: целевой файл
    :return: дата в формате float (секунды UNIX)
    """
    return os.stat(file).st_mtime


def func_num_of_files(max_num, directory):
    """
    считает число файлов в целевой папке, и возвращает boolean
    в зависимости больше ли число файлов заданного числа
    :param max_num: заданное число файлов
    :param directory: целевая папка
    :return: boolean, больше или меньше посчитанное число файлов
    """
    cur_num = len([name for name in os.listdir(directory)
                   if os.path.isfile(os.path.join(directory, name))])
    if cur_num > max_num:
        return True
    else:
        return False


def date_of_file(directory, old=False):
    """
    выполняет поиск самого нового (старого) файла в целевой папке
    :param directory: целевая папка для поиска
    :param old: если True, то ищем самый старый файл
    :return: возвращается кортеж с именем файла и датой создания
    """
    files = os.listdir(directory)
    files = [os.path.join(directory, file) for file in files]
    files = [file for file in files if os.path.isfile(file)]
    if files:
        if old:
            value = min(files, key=func_birthday)
        else:
            value = max(files, key=func_birthday)
        return value, func_birthday(value)
    else:
        value = 'folder is empty'
        date = 433082400.0
        return value, date


def func_is_changed(directory):
    """
    определяет были ли изменения в целевой папке
    :param directory: целевая папка
    :return: boolean - были ли изменения в целевой папке
    """
    is_changes = False
    new_hash = hashlib.md5()
    for dirpath, dirnames, filenames in os.walk(directory, topdown=True):
        dirnames.sort(key=os.path.normcase)
        filenames.sort(key=os.path.normcase)
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            new_hash.update(os.path.normcase(os.path.relpath(filepath, directory)).encode('utf-8'))
            f = open(filepath, 'rb')
            for chunk in iter(lambda: f.read(65536), b''):
                new_hash.update(chunk)
    logging.debug(f'new hash = {new_hash.hexdigest()}')
    if os.path.exists('./hashmd5'):
        with open('./hashmd5', 'r') as f:
            cur_hash = f.read()
            logging.debug(f'current hash = {cur_hash}')
        if cur_hash != new_hash.hexdigest():
            logging.debug('the hashes is NOT equal')
            with open('./hashmd5', 'w') as f:
                f.write(new_hash.hexdigest())
            is_changes = True
    else:
        with open('./hashmd5', 'w+') as f:
            logging.debug('new hash is created')
            f.write(new_hash.hexdigest())
            is_changes = True
    return is_changes


if __name__ == '__main__':
    logging.basicConfig(
        filename='archive.log',
        level=logging.DEBUG,
        format='{asctime} {name} {levelname} {message}',
        datefmt='%Y-%m-%d %H:%M:%S',
        style='{'
    )
    logging.debug('='*50)
    # Определяем текущее время
    cur_time = time.time()
    # Определяем самый свежий файл и время его создания
    last_in_1day, f_time = date_of_file(archive_1day)
    logging.debug(f'cur_time = {time.ctime(cur_time)}')
    logging.debug(f'f_time = {time.ctime(f_time)}')
    # Опеределяем сколько дней прошло, после создания самого свежего файла
    period = timedelta(seconds=cur_time - f_time)
    logging.debug(f'days = {period.days}')
    # Если прошло более 1 дня, делаем новый архив
    if period.days > 0:
        # Определяем были ли изменения в папке, после предыдущего раза
        if func_is_changed(archive_target):
            # Создаем архив по заданным параметрам
            shutil.make_archive(file_name, archive_format, archive_target)
            logging.debug(f'{file_name=} is created')
        else:
            logging.debug(f'hash is actual')
            exit('\nthere are NO changes in the target folder\n')
    else:
        logging.debug(f'file {last_in_1day} is actual')
        exit(f'\narchive finish\nfile {last_in_1day} is actual\n')

    if func_num_of_files(3, archive_1day):
        first_in_1day, f_time = date_of_file(archive_1day, old=True)
        logging.debug(f'{first_in_1day=}')
        logging.debug(f'time={time.ctime(f_time)}')
        last_in_3day, l_time = date_of_file(archive_3day)
        logging.debug(f'{last_in_3day=}')
        logging.debug(f'time={time.ctime(l_time)}')
        period = timedelta(seconds=f_time - l_time)
        logging.debug(f'days = {period.days}')
        if period.days >= 3:
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
        period = timedelta(seconds=f_time - l_time)
        logging.debug(f'days = {period.days}')
        if period.days >= 7:
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
        period = timedelta(seconds=f_time - l_time)
        logging.debug(f'days = {period.days}')
        if period.days >= 30:
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
        if period.days >= 30 * 3:
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
        if period.days >= 30 * 6:
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
