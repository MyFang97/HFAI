import os

from flask import Flask
import requests
import base64
import json

app = Flask(__name__)

# 百度人脸识别请求接口
BD_request_url = "https://aip.baidubce.com/rest/2.0/face/v3/detect"
static_image_url = 'D:\Desktop\HFAI\static'


def getImgB64(imageUrl):
    """
    获取图片base64编码
    :param imageUrl: 图片路径
    :return:
    """
    # img_path = 'face.jpg'
    f_img = open(imageUrl, 'rb')  # 二进制方式打开图文件
    ls_f = base64.b64encode(f_img.read())  # 读取文件内容，转换为base64编码
    f_img.close()
    return ls_f


def getBdAccessToken():
    """
    获取百度AItoken
    client_id 为官网获取的AK， client_secret 为官网获取的SK
    :return: access_token
    """
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=qGadE2QPlgHQnQXawp6PG6DD&client_secret=SGOv81lUOnYKVPiqvXN0yx4evwDOTtpl'
    response = requests.get(host)
    # if response:
    return response.json()['access_token']


access_token = getBdAccessToken()


# @app.route('/AI')
def BDAI_Face(imageUrl, access_token):
    """
    百度AI人脸识别接口
    :param imageUrl:图片路径
    :param access_token:百度access_token
    :return:
    """
    params = {'image': getImgB64(imageUrl),
              'image_type': 'BASE64',
              'face_field': 'age,beauty,expression,face_shape,gender,glasses,'
                            'landmark,landmark150,race,quality,eye_status,emotion,'
                            'face_type,mask,spoofing'}

    # access_token = getBdAccessToken()
    request_url = BD_request_url + "?access_token=" + access_token
    headers = {'content-type': 'application/json'}
    response = requests.post(request_url, data=params, headers=headers)
    if response:
        return response.json()


@app.route('/')
def hello_world():
    data = BDAI_Face(os.path.join(static_image_url, 'face.jpg'), access_token)
    return json.dumps(data)
    # return data['result']


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)
