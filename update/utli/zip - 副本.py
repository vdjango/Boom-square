import zipfile
import os
import shutil


version = '0.0.0'
name = 'Boom-square-' + version


def update_zip():

    filename = 'file.zip'
    fz = zipfile.ZipFile(filename, 'r')

    for file in fz.namelist():
        fz.extract(file, './')

    update_file()


def rmmove(srcPath='./', dstPath='update-version'):
    if os.path.exists(dstPath):
        shutil.rmtree(dstPath)
        os.mkdir(dstPath)
    else:
        os.mkdir(dstPath)

    for item in os.listdir(srcPath):
        if item != dstPath:

            if item != 'db.sqlite3':
                if item != 'file.zip':
                    if item != '.git':
                        print('DBA', item)
                        FilePath = os.path.join(srcPath, item)
                        if os.path.isdir(FilePath):
                            # 文件
                            dstAddPath = os.path.join(dstPath, item)
                            if os.path.exists(dstAddPath):
                                print('copyfile', FilePath, dstAddPath)
                                shutil.copyfile(FilePath, dstAddPath)
                            else:
                                print('copytree', FilePath, dstAddPath)
                                shutil.copytree(FilePath, dstAddPath)
                                shutil.rmtree(FilePath)
                        else:
                            print('move', FilePath, dstPath)
                            shutil.move(FilePath, dstPath)

    # os.rmdir(srcPath)


def update_file(srcPath='update-version/' + name, dstPath='./'):

    rmmove(dstPath)

    for item in os.listdir(srcPath):
        FilePath = os.path.join(srcPath, item)
        if os.path.isdir(FilePath):
            # 文件
            dstAddPath = os.path.join(dstPath, item)
            if os.path.exists(dstAddPath):
                print('copyfile', FilePath, dstAddPath)
                shutil.copyfile(FilePath, dstAddPath)
            else:
                print('copytree', FilePath, dstAddPath)
                shutil.copytree(FilePath, dstAddPath, False)
                shutil.rmtree(FilePath)
        else:
            print('copytree', FilePath, dstPath)
            shutil.move(FilePath, dstPath)

    os.rmdir(srcPath)
