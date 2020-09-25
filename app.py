import os

from flask import Flask
import requests
import base64
import json

from BaiDuAi import BDAI_Face, access_token
from utils import static_image_url

app = Flask(__name__)
# app.utils.from_object(utils)
# app.utils.from_pyfile('utils.py')

@app.route('/')
def hello_world():
    # print('hi')
    return '欢迎来到我们的世界'


@app.route('/api/bdai')
def baiDuAi():
    data = BDAI_Face(os.path.join(static_image_url, 'face.jpg'), access_token)
    return json.dumps(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999, debug=True)
