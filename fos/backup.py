# -*- coding:utf-8 -*-
'''
System Backup Tool
@author: Ben
Created on 2013-4-13
Copyright (c) 2012-2013 ZCTT.Co.Ltd. All rights reserved.
'''

import os
import stat
import time, shutil

def start(src_path, dst_path, isremoved=False):
    ''' backup src_path into dst_path. Compared file create or update time and copy updated file into dst_path
    Args:
        src_path - source file path. directory or file.
        dst_path - destination file path. directory or file. if destination file path is not existed, auto make it.
        isremoved - 
    '''
    if not src_path or not dst_path: return;
    
    # check dest directory existed
    if not os.path.exists(src_path): return;
    if not os.path.exists(dst_path): os.makedirs(dst_path)
    
    # traverse dest directory, compared every file with the source directory.
    # compared by file create or update time
    src_filename = ''
    if os.path.isfile(src_path) or os.path.islink(src_path):
        src_filename = os.path.basename(src_path)
        src_path = os.path.dirname(src_path)
    dst_file_table = __build_file_table(dst_path)
    src_file_list = [src_filename]
    index = 0
    while index < len(src_file_list):
        src_file = src_file_list[index]
        src_file_path = os.path.join(src_path, src_file)
        if dst_file_table.has_key(src_file): dst_file_table[src_file] = 1
        if os.path.isdir(src_file_path):
            # if it's directory, traverse his children
            file_names = os.listdir(src_file_path)
            for file_name in file_names:
                src_file_list.append(os.path.join(src_file, file_name))
        else:
            # if it's file
            isCopy = True
            if dst_file_table.has_key(src_file):
                # compared file modified time last
                dst_file_mtime = os.path.getmtime(os.path.join(dst_path, src_file))
                src_file_mtime = os.path.getmtime(os.path.join(src_path, src_file))
                if src_file_mtime <= dst_file_mtime: isCopy = False
            if isCopy:
                cp_dst_dir = os.path.dirname(os.path.join(dst_path, src_file))
                if not os.path.exists(cp_dst_dir):
                    os.makedirs(cp_dst_dir)
                shutil.copy(os.path.join(src_path, src_file), cp_dst_dir)
        index += 1    
        
    # delete files which are not in source directory but in destination directory
    if isremoved:
        for key in dst_file_table.keys():
            if dst_file_table[key] == 0:
                rm_path = os.path.join(dst_path, key)
                if os.path.isdir(rm_path): os.removedirs(rm_path)
                else: os.remove(rm_path)
         
    
def __build_file_table(file_path):
    file_table = {}
    file_list = ['']
    index = 0
    while index < len(file_list):
        cur_file = file_list[index]
        cur_file_path = os.path.join(file_path, cur_file)
        if os.path.isdir(cur_file_path):
            file_names = os.listdir(cur_file_path)
            for file_name in file_names:
                cur_file_path = os.path.join(cur_file_path, file_name)
                #if os.path.isfile(cur_file_path) or os.path.islink(cur_file_path):
                file_table[os.path.join(cur_file, file_name)] = 0
                file_list.append(os.path.join(cur_file, file_name))
        index += 1
            
    return file_table

    
if __name__ == '__main__':
    import sys
    if len(sys.argv) < 3: 
        print ' backup {source path} {dest path} '
        sys.exit(-1)
    
    start(sys.argv[1], sys.argv[2])
