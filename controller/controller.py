#-*- coding:utf-8 -*-

from django.http import HttpResponse
import codecs
import json
import os
from django.views.decorators.csrf import csrf_exempt
import random
from datetime import *

ROOT = os.path.dirname(__file__)

TID = 0
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
    nnn = "%s+%s" % (TID, dt.strftime(
        "%Y-%m-%d-%M-%H-%S-{0}{1}".format(random.randint(1, 999999), ext)))
    return nnn

# 读取json文件


def getConfigContent():
    jsonfile = open(ROOT + "/ueconfig.json")
    content = json.load(jsonfile)
    return content

# 上传配置类


class UploadConfig(object):
    def __init__(self, PathFormat, UploadFieldName, SizeLimit, AllowExtensions, SavePath, Base64, Base64Filename):
        super(UploadConfig, self).__init__()

        global TID

        from app.utli.datetimenow import datetime_ymd
        TIME = datetime_ymd()

        if '{{tid}}' in SavePath:
            webUrl = str(SavePath).split(
                '{{tid}}')[0] + TID + '/'

        self.PathFormat = PathFormat
        self.UploadFieldName = UploadFieldName
        self.SizeLimit = SizeLimit
        self.AllowExtensions = AllowExtensions
        self.SavePath = webUrl
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
def uploadFile(request, config):
    global TID
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

        # try:

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
        # except Exception as e:
        #    result.error = u"网络错误"
        #    return HttpResponse(buildJsonResult(result))


def listFileManage(request, imageManagerListPath, imageManagerAllowFiles, listsize):
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
    if '{{tid}}' in localPath:
        localPath = str(localPath).split(
            '{{tid}}')[0] + TID + '/'

    print('imagename', localPath)

    filelist = []
    exts = list(imageManagerAllowFiles)
    index = start
    list_dirs = os.walk(localPath)
    for root, dirs, files in list_dirs:
        for d in files:
            name, ext = os.path.splitext(d)
            if ext in exts:
                filelist.append(dict(url=d))
                index += 1
                if index - start >= size:
                    break

    jsondata = {"state": "SUCCESS", "list": filelist,
                "start": start, "size": size, "total": index}
    return HttpResponse(json.dumps(jsondata))


# 返回配置信息
def configHandler(request):
    content = getConfigContent()
    callback = request.GET.get("callback")

    imageUrlPrefix = content['imageUrlPrefix']
    fileUrlPrefix = content['fileUrlPrefix']
    videoUrlPrefix = content['videoUrlPrefix']
    fileManagerListPath = content['fileManagerListPath']
    imageManagerListPath = content['imageManagerListPath']

    imageManagerUrlPrefix = content['imageManagerUrlPrefix']

    global TID

    from app.utli.datetimenow import datetime_ymd
    TIME = datetime_ymd()

    if '{{tid}}' in imageUrlPrefix:
        imageUrlPrefix = str(imageUrlPrefix).split(
            '{{tid}}')[0] + TID + '/'

    if '{{tid}}' in fileUrlPrefix:
        fileUrlPrefix = str(fileUrlPrefix).split(
            '{{tid}}')[0] + TID + '/'

    if '{{tid}}' in fileUrlPrefix:
        videoUrlPrefix = str(videoUrlPrefix).split(
            '{{tid}}')[0] + TID + '/'

    if '{{tid}}' in fileManagerListPath:
        fileManagerListPath = str(fileManagerListPath).split(
            '{{tid}}')[0] + TID + '/'

    if '{{tid}}' in imageManagerListPath:
        imageManagerListPath = str(imageManagerListPath).split(
            '{{tid}}')[0] + TID + '/'

    if '{{tid}}' in imageManagerUrlPrefix:
        imageManagerUrlPrefix = str(imageManagerUrlPrefix).split(
            '{{tid}}')[0] + TID + '/'

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
        "filePathFormat": content["filePathFormat"],
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
        "fileManagerUrlPrefix": content["fileManagerUrlPrefix"],
        "fileManagerListSize": content["fileManagerListSize"],
        "fileManagerAllowFiles": content["fileManagerAllowFiles"]
    }

    if callback:
        return HttpResponse("{0}{1}".format(callback, json.dumps(dic)))
    return HttpResponse(json.dumps(dic))

# 图片上传控制


@csrf_exempt
def uploadimageHandler(request):
    UploadFieldName = GetConfigValue("imageFieldName")
    SizeLimit = GetConfigValue("imageMaxSize")
    AllowExtensions = GetConfigValue("imageAllowFiles")

    PathFormat = GetConfigValue("imagePathFormat")
    SavePath = GetConfigValue("imageUrlPrefix")

    upconfig = UploadConfig(PathFormat, UploadFieldName,
                            SizeLimit, AllowExtensions, SavePath, False, '')

    return uploadFile(request, upconfig)


def uploadvideoHandler(request):
    AllowExtensions = GetConfigValue("videoAllowFiles")
    PathFormat = GetConfigValue("videoPathFormat")
    SizeLimit = GetConfigValue("videoMaxSize")
    UploadFieldName = GetConfigValue("videoFieldName")
    SavePath = GetConfigValue("videoUrlPrefix")
    upconfig = UploadConfig(PathFormat, UploadFieldName,
                            SizeLimit, AllowExtensions, SavePath, False, '')
    return uploadFile(request, upconfig)


def uploadfileHandler(request):
    AllowExtensions = GetConfigValue("fileAllowFiles")
    PathFormat = GetConfigValue("filePathFormat")
    SizeLimit = GetConfigValue("fileMaxSize")
    UploadFieldName = GetConfigValue("fileFieldName")
    SavePath = GetConfigValue("fileUrlPrefix")
    upconfig = UploadConfig(PathFormat, UploadFieldName,
                            SizeLimit, AllowExtensions, SavePath, False, '')
    return uploadFile(request, upconfig)


# 在线图片
def listimageHandler(request):
    imageManagerListPath = GetConfigValue("imageManagerListPath")  # 路径
    imageManagerAllowFiles = GetConfigValue("imageManagerAllowFiles")  # 类型
    imagelistsize = GetConfigValue("imageManagerListSize")  # 大小
    return listFileManage(request, imageManagerListPath, imageManagerAllowFiles, imagelistsize)


# 在线文件

def ListFileManagerHander(request):
    fileManagerListPath = GetConfigValue("fileManagerListPath")
    fileManagerAllowFiles = GetConfigValue("fileManagerAllowFiles")
    filelistsize = GetConfigValue("fileManagerListSize")
    return listFileManage(request, fileManagerListPath, fileManagerAllowFiles, filelistsize)


def deleteimageHandler(request):
    # /controller/?action=imgdel&del=20180301471736412080.png
    global TID

    image = request.GET.get('img_name')
    path = GetConfigValue("imageUrlPrefix")

    ath = str(image).split('+')[0]

    if '{{tid}}' in path:
        path = str(path).split('{{tid}}')[0] + str(ath) + '/' + image
        path = ROOT + path
        os.remove(path)
        print('path', path)
        pass

    # return path


actions = {
    "config": configHandler,
    "uploadimage": uploadimageHandler,
    "uploadvideo": uploadvideoHandler,
    "uploadfile": uploadfileHandler,
    "listimage": listimageHandler,
    "listfile": ListFileManagerHander,
    "imageDelUrl": deleteimageHandler,
}


@csrf_exempt
def handler(request, tid=None):
    global TID
    TID = tid
    print('value', TID)
    action = request.GET.get("action")
    return actions.get(action)(request)
