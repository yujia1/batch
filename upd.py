import ctypes
import os
import time
import sys
from hurry.filesize import size
import logging

logging.basicConfig(filename ='UPDFileClean.log', level = logging.INFO, format ='%(asctime)s - %(message)s')

def day_ago(num_day):
    '''
    Function converts how many days ago to how many seconds ago.
    input is numbers either an integer or a float, in day.
    output is numbers, in seconds.
    '''
    return time.time() - (num_day * 24 * 60 * 60)

def remove_file(path, num_day, extend):
    '''
    Function removes the file with extend by days ago, which is located in repository's path.
    the input of path starts by r + path of repository,
    the input of num_day is assgined to function day_ago,
    the input of extend is type of file(ex: .pdf).
    the output is void, and delete target files.
    '''
    directory = path[0:3]
    file_size_before = get_free_space(directory)
    
    # os.path.getsize(path)# track size of directory before delete UPD files
    # sum(os.path.getsize(f) for f in os.listdir('.') if os.path.isfile(f))
    total_size = 0
    dir_name = path
    items = os.listdir(dir_name)  # list all file in repository
    for item in items:
        file = os.path.join(dir_name, item)  # join file with root
        if item.endswith(extend):  # select file by type
            if os.stat(file).st_mtime < day_ago(num_day):  ## select file before the day ago
                total_size += os.path.getsize(file)  ## Gives the size in bytes
                os.remove(file)  # delete file
    file_size_estimate = file_size_before - total_size
    file_size_after = get_free_space(directory)
    # file_size(path)
    # os.path.getsize(path)# track size of directory after delete UPD files
    # sum(os.path.getsize(f) for f in os.listdir('.') if os.path.isfile(f))
    logging.info("Before UPD files are deleted, G:\ drive free space: " + size(file_size_before))
    logging.info("After UPD files are deleted, G:\ drive free space : " + size(file_size_after))
    logging.info("Total deleted UPD files size: " + size(total_size))  ## size automatically covert bytes to MB or GB
    logging.info("===========================================================")
def get_free_space(dirname):
    """Return folder/drive free space (in megabytes)."""
    
    free_bytes = ctypes.c_ulonglong(0)
    ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dirname), None, None, ctypes.pointer(free_bytes))
    return free_bytes.value 

def get_size(path):
    total_size = 0
    for dirpath,dirnames,filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath,f)
            total_size += os.path.getsize(fp)
    return total_size

if __name__ == '__main__':
    '''
    in window systtem, use \; in os system, use /
    '''
    remove_file(r'G:\blp\Wintrv',10,'.upd')
    #remove_file(r'/Users/hangxigudeaoqi/Desktop/test', 30, '.pdf')
