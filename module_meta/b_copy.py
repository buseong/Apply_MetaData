import os
import shutil


def copy_file(target_1, target):
    folder = target.replace("\\", "/") + '/'
    now_file_edit = []
    name_list = []
    for i in os.listdir(folder):
        if os.path.splitext(i)[1] == '.mp3':
            now_file_edit.append(folder + i)
            name_list.append(os.path.splitext(i)[0] + '.mp3')
    for j in enumerate(name_list):
        j = j[0]
        shutil.copy(now_file_edit[j], target_1 + name_list[j])
    return
