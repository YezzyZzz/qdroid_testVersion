import os
import shutil
from datetime import datetime
import logging
logger = logging.getLogger()


def get_json(file_path, data):
    try:
        f = open(file_path, "w")
        for key, val in data.items():
            for v in val:
                print(str(key) + '_' + str(v), file=f)
    except Exception as e:
        logger.error(e)
        logger.error("fail to write json data.")
    else:
        logger.info("json data of " + file_path + " written successfully.")
    f.close()


def get_file_size(file_path):
    file_size = os.path.getsize(file_path)
    file_size = file_size / float(1024 * 1024)
    return str(round(file_size, 2)) + "MB"


def get_file_list(file_path):
    '''

    :return: all the path of the files of the param('file_path')
    '''
    import os
    file_name = list()
    for i in os.listdir(file_path):
        data_collect = ''.join(i)
        file_name.append(file_path + "/" + data_collect)
    return file_name


def get_file_list_full(file_path, res_list):
    for root, dirs, files in os.walk(file_path):
        for file in files:
            file = root + "//" + file
            res_list.append(file)


def copy_file(src_file, des_path):
    '''
    this function is used for the copy operation
    :param src_file:    the file that you want to move
    :param des_path:    the file that you want to move to
    :return:
    '''
    if not os.path.isfile(src_file):
        print("%s not exist!" % src_file)
    else:
        file_path, file_name = os.path.split(src_file)
        if not os.path.exists(des_path):
            os.makedirs(des_path)
            print("copy %s -> %s" % (src_file, des_path + file_name))
        shutil.copy(src_file, des_path + file_name)


def get_meta_data(meta, info_line):
    res = ""
    info_line = info_line[info_line.find(meta):]
    info_line = info_line.replace(meta, "")
    res = info_line[info_line.find("'") + 1:]
    res = res[:res.find("'")]
    return res


def show_progress(cnt, total, time_pre_block):
    time_pre = time_pre_block[0]
    time_now = datetime.now().strftime("%S")
    if int(time_now) - int(time_pre) >= 1 or cnt == total:
        print(str(cnt/total*100) + "%")
        time_pre_block[0] = time_now


def packing(apk, file_size, info_path):
    pkg_name = ""
    ver_code = ""
    ver_name = ""
    sdk_ver = ""
    target_sdk_ver = ""
    with open(info_path, "r", encoding="utf-8") as f:
        info = f.readlines()
    for info_line in info:
        info_line = info_line.replace("\n", "")
        if "package: name=" in info_line:
            pkg_name = get_meta_data("package: name=", info_line)
        if "versionCode=" in info_line:
            ver_code = get_meta_data("versionCode=", info_line)
        if "versionName=" in info_line:
            ver_name = get_meta_data("versionName=", info_line)
        if "sdkVersion:" in info_line:
            sdk_ver = get_meta_data("sdkVersion:", info_line)
        if "targetSdkVersion" in info_line:
            target_sdk_ver = get_meta_data("targetSdkVersion", info_line)
    apk.set_metadata(file_size, datetime.now().strftime('%Y-%m-%d'), pkg_name, ver_code, ver_name, sdk_ver, target_sdk_ver)