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
            if item != 'file.zip':
                if item != '.git':
                    FilePath = os.path.join(srcPath, item)
                    if os.path.isdir(FilePath):
                        # 文件
                        dstAddPath = os.path.join(dstPath, item)
                        if os.path.exists(dstAddPath):
                            shutil.copyfile(FilePath, dstAddPath)
                        else:
                            shutil.copytree(FilePath, dstAddPath)
                            shutil.rmtree(FilePath)
                    else:
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
                shutil.copyfile(FilePath, dstAddPath)
            else:
                shutil.copytree(FilePath, dstAddPath, False)
                shutil.rmtree(FilePath)
        else:
            shutil.move(FilePath, dstPath)

    os.rmdir(srcPath)
