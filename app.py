import os

from flask import Flask
import requests
import base64
import json

app = Flask(__name__)


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


@app.route('/')
def hello_world():
    return '欢迎来到我们的世界'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)
