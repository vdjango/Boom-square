import zipfile
import os
import shutil


version = '0.1.0'
name = 'Boom-square-' + version
error_list = []


def update_zip():

    filename = 'file.zip'
    fz = zipfile.ZipFile(filename, 'r')

    for file in fz.namelist():
        fz.extract(file, './')

    update_file()


def copyfile2(FilePath, dstAddPath):
    '''
    FilePath和dstAddPath都只能是文件
    '''
    print('copyfile', FilePath, dstAddPath)
    try:
        shutil.copyfile(FilePath, dstAddPath)
    except (IOError, os.error) as why:
        error_list.append(str(FilePath + ',' + dstAddPath + ',' + str(why)))

    except shutil.Error as err:
        error_list.extend(err.args[0])


def copytree2(FilePath, dstAddPath):
    '''
    FilePath和dstAddPath都只能是目录，且dstAddPath必须不存在
    '''
    print('copytree', FilePath, dstAddPath)

    try:
        shutil.copytree(FilePath, dstAddPath)
    except (IOError, os.error) as why:
        error_list.append(str(FilePath + ',' + dstAddPath + ',' + str(why)))

    except shutil.Error as err:
        error_list.extend(err.args[0])


def rmtree2(FilePath):
    '''
    空目录、有内容的目录都可以删
    '''
    print('rmtree', FilePath)
    try:
        shutil.rmtree(FilePath)
    except (IOError, os.error) as why:
        error_list.append(str(FilePath + ',' + str(why)))

    except shutil.Error as err:
        error_list.extend(err.args[0])


def move2(FilePath, dstPath):
    '''
    移动文件
    '''
    print('move', FilePath, dstPath)
    try:
        shutil.move(FilePath, dstPath)
    except (IOError, os.error) as why:
        error_list.append(str(FilePath + ',' + dstPath + ',' + str(why)))

    except shutil.Error as err:
        error_list.extend(err.args[0])


def rmmove(srcPath='./', dstPath='update-version'):
    if os.path.exists(dstPath):
        shutil.rmtree(dstPath)
        os.mkdir(dstPath)
    else:
        os.mkdir(dstPath)

    path_dis = []

    for item in os.listdir(srcPath):
        if item != dstPath:
            if item != 'file.zip':
                if item != 'db.sqlite3':
                    path_dis.append(item)

    for line in path_dis:
        FilePath = os.path.join(srcPath, line)
        if os.path.isdir(FilePath):
            # 目录
            print('目录', FilePath)
            dstAddPath = os.path.join(dstPath, line)
            if os.path.exists(dstAddPath):
                # 目录文件存在
                print('目录文件存在', FilePath)
                copyfile2(FilePath, dstAddPath)
            else:
                # 目录文件不存在
                print('目录文件不存在', FilePath)
                copytree2(FilePath, dstAddPath)

            # rmtree2(FilePath)

        else:
            # 文件
            print('文件', FilePath)
            move2(FilePath, dstPath)

    # os.rmdir(srcPath)


def update_file(srcPath='update-version/' + name, dstPath='./'):

    rmmove(dstPath)

    for item in os.listdir(srcPath):
        FilePath = os.path.join(srcPath, item)
        if os.path.isdir(FilePath):
            # 目录
            print('目录', FilePath)
            dstAddPath = os.path.join(dstPath, item)
            if os.path.exists(dstAddPath):
                # 目录文件存在
                print('目录文件存在', FilePath)
                copyfile2(FilePath, dstAddPath)
            else:
                # 目录文件不存在
                print('目录文件不存在', FilePath)
                copytree2(FilePath, dstAddPath)

            rmtree2(FilePath)

        else:
            # 文件
            print('文件', FilePath)
            move2(FilePath, dstPath)

    rmtree2(srcPath)
