# 百度人脸识别请求接口
import requests
from utils import getImgB64

BD_request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"


def getBdAccessToken():
    """
    获取百度AItoken
    client_id 为官网获取的AK， client_secret 为官网获取的SK
    :return: access_token
    """
    host = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=qGadE2QPlgHQnQXawp6PG6DD&client_secret=SGOv81lUOnYKVPiqvXN0yx4evwDOTtpl"
    response = requests.get(host)
    # if response:
    return response.json()["access_token"]


def BDAI_Face(imageUrl, access_token):
    """
    百度AI人脸识别接口
    :param imageUrl:图片路径
    :param access_token:百度access_token
    :return:
    """
    params = {
        "image": getImgB64(imageUrl),
        "image_type": "BASE64",
        "face_field": "age,beauty,expression,face_shape,gender,glasses,"
                      "landmark,landmark150,race,quality,eye_status,emotion,"
                      "face_type,mask,spoofing",
    }

    # access_token = getBdAccessToken()
    request_url = BD_request_url + "?access_token=" + access_token
    headers = {"content-type": "application/json"}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        return response.json()


access_token = getBdAccessToken()
