#-*- coding:utf-8 -*-

from django.http import HttpResponse
import codecs
import json
import os
from django.views.decorators.csrf import csrf_exempt
import random
from datetime import *

from Boom_square.settings import BASE_DIR
ROOT = BASE_DIR

# ROOT = os.path.dirname(__file__)

# 本地上传图片时构造json返回值


class JsonResult(object):
    def __init__(self, state="未知错误", url="", title="", original="", error="null"):
        super(JsonResult, self).__init__()
        self.state = state
        self.url = url
        self.title = title
        self.original = original
        self.error = error

        print('JsonResult', state, url, title, original, error)


# 构造返回json


def buildJsonResult(result):
    jsondata = {"state": result.state, "url": result.url,
                "title": result.title, "original": result.original, "error": result.error}
    print('buildJsonResult', jsondata)
    return json.dumps(jsondata)


def buildFileName(filename):
    dt = datetime.now()
    name, ext = os.path.splitext(filename)

    return "%s" % (dt.strftime("%Y-%m-%d-%M-%H-%S-{0}{1}".format(random.randint(1, 999999), ext)))

# 读取json文件


def getConfigContent():
    jsonfile = open(ROOT + "/ueconfig.json")
    content = json.load(jsonfile)
    return content

# 上传配置类


class UploadConfig(object):
    def __init__(self, PathFormat, UploadFieldName, SizeLimit, AllowExtensions, SavePath, Base64, Base64Filename, tid_unix):
        super(UploadConfig, self).__init__()

        if '{{tid_unix}}' in SavePath:
            SavePath = str(SavePath).split(
                '{{tid_unix}}')[0] + tid_unix + '/'

        print('SavePath', SavePath)

        self.PathFormat = PathFormat
        self.UploadFieldName = UploadFieldName
        self.SizeLimit = SizeLimit
        self.AllowExtensions = AllowExtensions
        self.SavePath = SavePath
        self.Base64 = Base64
        self.Base64Filename = Base64Filename


# 获取json配置中的某属性值


def GetConfigValue(key):
    config = getConfigContent()
    return config[key]

# 检查文件扩展名是否在允许的扩展名内


def CheckFileType(filename, AllowExtensions):
    exts = list(AllowExtensions)
    name, ext = os.path.splitext(filename)
    return ext in exts


def CheckFileSize(filesize, SizeLimit):
    return filesize < SizeLimit

# 处理上传图片、文件、视频文件


@csrf_exempt
def uploadFile(request, config, tid_unix):
    result = JsonResult()
    if config.Base64:
        pass
    else:
        buf = request.FILES.get(config.UploadFieldName)

        filename = buf.name

        if not CheckFileType(filename, config.AllowExtensions):
            result.error = u"不允许的文件格式"
            print('error', '不允许的文件格式')
            return HttpResponse(buildJsonResult(result))

        if not CheckFileSize(buf.size, config.SizeLimit):
            result.error = u"文件大小超出服务器限制"
            print('error', '文件大小超出服务器限制')
            return HttpResponse(buildJsonResult(result))

        try:

            if not os.path.exists(ROOT + config.SavePath):
                os.makedirs(ROOT + config.SavePath)

            truelyName = buildFileName(filename)

            webUrl = config.SavePath + truelyName

            savePath = ROOT + webUrl

            f = codecs.open(savePath, "wb")
            for chunk in buf.chunks():
                f.write(chunk)

            f.flush()
            f.close()
            result.state = "SUCCESS"
            result.url = truelyName
            result.title = truelyName
            result.original = truelyName
            response = HttpResponse(buildJsonResult(result))
            response["Content-Type"] = "text/plain"
            return response
        except Exception as e:
            result.error = u"网络错误"
            return HttpResponse(buildJsonResult(result))


def listFileManage(request, tid_unix, imageManagerListPath, imageManagerAllowFiles, listsize):
    '''
    处理在线图片与在线文件
    返回的数据格式：
    {
        "state":"SUCCESS",
        "list":[
            {"url":"upload/image/20140627/6353948647502438222009315.png"},
            {"url":"upload/image/20140627/6353948659383617789875352.png"},
            {"url":"upload/image/20140701/6353980733328090063690725.png"},
            {"url":"upload/image/20140701/6353980745691597223366891.png"},
            {"url":"upload/image/20140701/6353980747586705613811538.png"},
            {"url":"upload/image/20140701/6353980823509548151892908.png"}
        ],
        "start":0,
        "size":20,
        "total":6
    }
    '''
    pstart = request.GET.get("start")
    start = pstart == None and int(pstart) or 0
    psize = request.GET.get("size")
    size = psize == None and int(GetConfigValue(listsize)) or int(psize)

    localPath = ROOT + imageManagerListPath
    if '{{tid_unix}}' in localPath:
        localPath = str(localPath).split('{{tid_unix}}')[0] + tid_unix + '/'

    filelist = []
    exts = list(imageManagerAllowFiles)
    index = start
    list_dirs = os.walk(localPath)
    for root, dirs, files in list_dirs:

        for d in files:
            name, ext = os.path.splitext(d)

            if ext in exts:
                filelist.append(dict(url=d))
                print('filelist', filelist)
                index += 1
                if index - start >= size:
                    break

    jsondata = {"state": "SUCCESS", "list": filelist,
                "start": start, "size": size, "total": index}
    return HttpResponse(json.dumps(jsondata))


# 返回配置信息
def configHandler(request, tid_unix):
    content = getConfigContent()
    callback = request.GET.get("callback")

    imageUrlPrefix = content['imageUrlPrefix']
    fileUrlPrefix = content['fileUrlPrefix']
    videoUrlPrefix = content['videoUrlPrefix']
    fileManagerListPath = content['fileManagerListPath']
    fileManagerUrlPrefix = content['fileManagerUrlPrefix']

    imageManagerListPath = content['imageManagerListPath']
    imageManagerUrlPrefix = content['imageManagerUrlPrefix']

    if '{{tid_unix}}' in imageUrlPrefix:
        imageUrlPrefix = str(imageUrlPrefix).split(
            '{{tid_unix}}')[0] + tid_unix + '/'

    if '{{tid_unix}}' in fileUrlPrefix:
        fileUrlPrefix = str(fileUrlPrefix).split(
            '{{tid_unix}}')[0] + tid_unix + '/'

    if '{{tid_unix}}' in videoUrlPrefix:
        videoUrlPrefix = str(videoUrlPrefix).split(
            '{{tid_unix}}')[0] + tid_unix + '/'

    if '{{tid_unix}}' in fileManagerListPath:
        fileManagerListPath = str(fileManagerListPath).split(
            '{{tid_unix}}')[0] + tid_unix + '/'

    if '{{tid_unix}}' in fileManagerUrlPrefix:
        fileManagerUrlPrefix = str(fileManagerUrlPrefix).split('{{tid_unix}}')[
            0] + tid_unix + '/'

    if '{{tid_unix}}' in imageManagerListPath:
        imageManagerListPath = str(imageManagerListPath).split('{{tid_unix}}')[
            0] + tid_unix + '/'

    if '{{tid_unix}}' in imageManagerUrlPrefix:
        imageManagerUrlPrefix = str(imageManagerUrlPrefix).split('{{tid_unix}}')[
            0] + tid_unix + '/'

    dic = {
        "imageActionName": content["imageActionName"],
        "imageFieldName": content["imageFieldName"],
        "imageMaxSize": content["imageMaxSize"],
        "imageAllowFiles": content["imageAllowFiles"],
        "imageCompressEnable": content["imageCompressEnable"],
        "imageCompressBorder": content["imageCompressBorder"],
        "imageInsertAlign": content["imageInsertAlign"],
        "imageUrlPrefix": imageUrlPrefix,
        "imagePathFormat": content["imagePathFormat"],

        "imageDelUrl": content["imageDelUrl"],

        "scrawlActionName": content["scrawlActionName"],
        "scrawlFieldName": content["scrawlFieldName"],
        "scrawlPathFormat": content["scrawlPathFormat"],
        "scrawlMaxSize": content["scrawlMaxSize"],
        "scrawlUrlPrefix": content["scrawlUrlPrefix"],
        "scrawlInsertAlign": content["scrawlInsertAlign"],

        "snapscreenActionName": content["snapscreenActionName"],
        "snapscreenPathFormat": content["snapscreenPathFormat"],
        "snapscreenUrlPrefix": content["snapscreenUrlPrefix"],
        "snapscreenInsertAlign": content["snapscreenInsertAlign"],

        "catcherLocalDomain": content["catcherLocalDomain"],
        "catcherActionName": content["catcherActionName"],
        "catcherFieldName": content["catcherFieldName"],
        "catcherPathFormat": content["catcherPathFormat"],
        "catcherUrlPrefix": content["catcherUrlPrefix"],
        "catcherMaxSize": content["catcherMaxSize"],
        "catcherAllowFiles": content["catcherAllowFiles"],

        "videoActionName": content["videoActionName"],
        "videoFieldName": content["videoFieldName"],
        "videoPathFormat": content["videoPathFormat"],
        "videoUrlPrefix": videoUrlPrefix,
        "videoMaxSize": content["videoMaxSize"],
        "videoAllowFiles": content["videoAllowFiles"],

        "fileActionName": content["fileActionName"],
        "fileFieldName": content["fileFieldName"],
        "filePathFormat": fileUrlPrefix,
        "fileUrlPrefix": fileUrlPrefix,
        "fileMaxSize": content["fileMaxSize"],
        "fileAllowFiles": content["fileAllowFiles"],

        "imageManagerActionName": content["imageManagerActionName"],
        "imageManagerListPath": imageManagerListPath,
        "imageManagerListSize": content["imageManagerListSize"],
        "imageManagerUrlPrefix": imageManagerUrlPrefix,
        "imageManagerInsertAlign": content["imageManagerInsertAlign"],
        "imageManagerAllowFiles": content["imageManagerAllowFiles"],

        "fileManagerActionName": content["fileManagerActionName"],
        "fileManagerListPath": fileManagerListPath,
        # content["fileManagerUrlPrefix"],
        "fileManagerUrlPrefix": fileManagerUrlPrefix,
        "fileManagerListSize": content["fileManagerListSize"],
        "fileManagerAllowFiles": content["fileManagerAllowFiles"]
    }

    print('fileManagerListPath', fileManagerListPath)

    if callback:
        return HttpResponse("{0}{1}".format(callback, json.dumps(dic)))
    return HttpResponse(json.dumps(dic))

# 图片上传控制


@csrf_exempt
def uploadimageHandler(request, tid_unix):
    UploadFieldName = GetConfigValue("imageFieldName")
    SizeLimit = GetConfigValue("imageMaxSize")
    AllowExtensions = GetConfigValue("imageAllowFiles")

    PathFormat = GetConfigValue("imagePathFormat")
    SavePath = GetConfigValue("imageUrlPrefix")

    upconfig = UploadConfig(PathFormat, UploadFieldName,
                            SizeLimit, AllowExtensions, SavePath, False, '', tid_unix)

    return uploadFile(request, upconfig, tid_unix)


def uploadvideoHandler(request, tid_unix):
    AllowExtensions = GetConfigValue("videoAllowFiles")
    PathFormat = GetConfigValue("videoPathFormat")
    SizeLimit = GetConfigValue("videoMaxSize")
    UploadFieldName = GetConfigValue("videoFieldName")
    SavePath = GetConfigValue("videoUrlPrefix")
    upconfig = UploadConfig(PathFormat, UploadFieldName,
                            SizeLimit, AllowExtensions, SavePath, False, '', tid_unix)
    return uploadFile(request, upconfig, tid_unix)


def uploadfileHandler(request, tid_unix):
    AllowExtensions = GetConfigValue("fileAllowFiles")
    PathFormat = GetConfigValue("filePathFormat")
    SizeLimit = GetConfigValue("fileMaxSize")
    UploadFieldName = GetConfigValue("fileFieldName")
    SavePath = GetConfigValue("fileUrlPrefix")
    upconfig = UploadConfig(PathFormat, UploadFieldName,
                            SizeLimit, AllowExtensions, SavePath, False, '', tid_unix)
    return uploadFile(request, upconfig, tid_unix)


# 在线图片
def listimageHandler(request, tid_unix):
    imageManagerListPath = GetConfigValue("imageManagerListPath")  # 路径
    imageManagerAllowFiles = GetConfigValue("imageManagerAllowFiles")  # 类型
    imagelistsize = GetConfigValue("imageManagerListSize")  # 大小
    return listFileManage(request, tid_unix, imageManagerListPath, imageManagerAllowFiles, imagelistsize)


# 在线文件

def ListFileManagerHander(request, tid_unix):
    fileManagerListPath = GetConfigValue("fileManagerListPath")
    fileManagerAllowFiles = GetConfigValue("fileManagerAllowFiles")
    filelistsize = GetConfigValue("fileManagerListSize")
    return listFileManage(request, tid_unix, fileManagerListPath, fileManagerAllowFiles, filelistsize)


def deleteimageHandler(request, tid_unix=None):
    err = "null"
    SUCCESS = "SUCCESS"
    image = request.POST.get("path")
    path = GetConfigValue("imageUrlPrefix")

    if '{{tid_unix}}' in path:
        print('path', image)
        path = str(path).split('{{tid_unix}}')[0] + str(tid_unix) + '/' + image
    else:
        path = str(path) + str(tid_unix) + '/' + image

    path = ROOT + path
    print('path', path)
    try:
        os.remove(path)
    except Exception as e:
        err = "删除失败"
        SUCCESS = "删除失败"
        raise e

    jsondata = {"state": str(SUCCESS), "url": str(image),
                "title": str(image), "original": str(image), "error": str(err)}
    print('buildJsonResult', jsondata)
    return HttpResponse(json.dumps(jsondata))


def deletefileHandler(request, tid_unix=None):
    # /controller/?action=imgdel&del=20180301471736412080.png
    err = "null"
    SUCCESS = "SUCCESS"
    image = request.POST.get("path")
    path = GetConfigValue("fileUrlPrefix")

    if '{{tid_unix}}' in path:
        print('path', image)
        path = str(path).split('{{tid_unix}}')[0] + str(tid_unix) + '/' + image
    else:
        path = str(path) + str(tid_unix) + '/' + image

    path = ROOT + path
    print('path', path)
    try:
        os.remove(path)
    except Exception as e:
        err = "删除失败"
        SUCCESS = "删除失败"
        raise e

    jsondata = {"state": str(SUCCESS), "url": str(image),
                "title": str(image), "original": str(image), "error": str(err)}
    print('buildJsonResult', jsondata)
    return HttpResponse(json.dumps(jsondata))


actions = {
    "config": configHandler,
    "uploadimage": uploadimageHandler,
    "uploadvideo": uploadvideoHandler,
    "uploadfile": uploadfileHandler,
    "listimage": listimageHandler,
    "listfile": ListFileManagerHander,
    "deleteimage": deleteimageHandler,
    "deletefile": deletefileHandler,
}


@csrf_exempt
def handler(request, tid=None):
    unix = request.GET.get('unix')

    print('XXXXXXXXXX', unix)

    action = request.GET.get("action")

    return actions.get(action)(request, unix)
