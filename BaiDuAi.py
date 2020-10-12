# 百度人脸识别请求接口
import requests
from utils import getImgB64
import logging

def getBdAccessToken():
    """
    获取百度AItoken
    client_id 为官网获取的AK， client_secret 为官网获取的SK
    :return: access_token
    """
    host = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=DGNYtO6GyGOjNuGgggoi4ZPN&client_secret=vl28C4qIV3GbGwWMo9WNPNsB3Yc8SqKQ"
    response = requests.get(host)
    # if response:
    return response.json()["access_token"]


access_token = getBdAccessToken()


def BDAI_Face(imageUrl):
    """
    百度AI人脸属性识别接口
    :param imageUrl:图片路径
    :param access_token:百度access_token
    :return:
    """
    Bd_Face_request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
    params = {
        "image":
        getImgB64(imageUrl),
        "image_type":
        "BASE64",
        "face_field":
        "age,beauty,expression,face_shape,gender,glasses,"
        "landmark,landmark150,race,quality,eye_status,emotion,"
        "face_type,mask,spoofing",
    }

    # access_token = getBdAccessToken()
    request_url = Bd_Face_request_url + "?access_token=" + access_token
    headers = {"content-type": "application/json"}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        return response.json()


def BDAI_Poem(word):
    """
    百度AI根据关键词自动生成7言绝句
    word：关键词
    """
    Bd_Poen_request_url = "https://aip.baidubce.com/rpc/2.0/creation/v1/poem"
    headers = {'Content-Type':'application/json'}
    index = 0
    params = {
        'text' : word.encode('utf-8'),
        'index' : index
    }
    logging.info('params:{}'.format(params))
    request_url = Bd_Poen_request_url + "?access_token=" + access_token
    headers = {"content-type": "application/json"}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        index += 1
        return response.json()
    