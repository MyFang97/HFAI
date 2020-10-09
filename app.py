import os
import cv2
from flask import Flask, request
import requests
import base64
import json
from BaiDuAi import BDAI_Face, access_token

import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.ERROR)
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(filename)s(%(funcName)s)[line:%(lineno)d] %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = Flask(__name__)


# static_image_url = '/home/ubuntu/HFAI/static/images'


@app.route("/")
def hello_world():
    # print('hi')
    return "欢迎来到我们的世界"


@app.route("/api/bdai", methods=['POST'])
def baiDuAi():
    image_path = request.form['image_path']
    app.logger.info('image_path:{}'.format(image_path))
    small_image_path = str(image_path).split('.')[0] + '_small' + str(image_path).split('.')[1]
    app.logger.info('small_image_path:{}'.format(small_image_path))
    res = BDAI_Face(image_path, access_token)
    logger.info('res:{}'.format(res))
    result = {}
    result["code"] = res["error_code"]  # 状态码
    result["msg"] = res["error_msg"]  # 消息
    if result["code"] == 0:
        result['data'] = {}
        result["data"]["face_num"] = res['result']["face_num"]  # 人脸数量

        # result["data"]["location"] = res['result']["face_list"][0][
        #     "location"]  # 人脸位置
        # 根据人脸位置获取小图并返回
        # getSmallImage(image_path, small_image_path, res['result']["face_list"][0][
        #     "location"])
        # result['data']['small_image_path'] = small_image_path

        result["data"]["age"] = res['result']["face_list"][0]["age"]  # 年龄
        result["data"]["beauty"] = res['result']["face_list"][0][
            "beauty"]  # 颜值
        result["data"]["expression"] = res['result']["face_list"][0][
            "expression"]["type"]  # 表情none:不笑；smile:微笑；laugh:大笑
        result["data"]["face_shape"] = res['result']["face_list"][0][
            "face_shape"][
            "type"]  # 脸型square: 正方形 triangle:三角形 oval: 椭圆 heart: 心形 round: 圆形
        result["data"]["gender"] = res['result']["face_list"][0]["gender"][
            "type"]  # male:男性 female:女性
        result["data"]["glasses"] = res['result']["face_list"][0]["glasses"][
            "type"]  # none:无眼镜，common:普通眼镜，sun:墨镜
        result["data"]["emotion"] = res['result']["face_list"][0]["emotion"][
            "type"]  # 情绪angry:愤怒 disgust:厌恶 fear:恐惧 happy:高兴 sad: 伤心 surprise: 惊讶 neutral: 无情绪
        result["data"]["race"] = res['result']["face_list"][0]["race"][
            "type"]  # 肤色yellow: 黄种人 white: 白种人 black:黑种人 arabs: 阿拉伯人
    app.logger.info('result:{}'.format(result))
    return json.dumps(result)


# 设置图片上传允许的文件格式
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'JPG', 'PNG', 'bmp'])


def allowed_file(filename):
    """
    设置允许上传图片格式
    :param filename:文件名
    :return:
    """
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def getSmallImage(big_image, small_image, bbox):
    '''
    获取小图图片
    :param big_image:大图路径
    :param small_image:小图路径
    :param bbox:小图坐标
    :return:
    '''
    img = cv2.imread(big_image, flags=cv2.IMREAD_COLOR)
    x = bbox[0]
    y = bbox[1]
    cut = img[int(y):int(bbox[3]), int(x):int(bbox[2])]
    cv2.imwrite(small_image, cut)


"""
上传图片路由，图片存储在static/images/
"""


@app.route('/api/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        result = {}
        f = request.files['file']
        if not (f and allowed_file(f.filename)):
            result['code'] = 1001
            result['msg'] = "请检查上传的图片类型，仅限于png、PNG、jpg、JPG、bmp"
            return json.dumps(result)
        logger.info('filename:{}'.format(f.filename))
        # 处理上传图片位置
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath, 'static/images', f.filename)  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        logger.info('upload_path:{}'.format(upload_path))
        # 使用Opencv转换一下图片格式和名称
        img = cv2.imread(upload_path)
        cv2.imwrite(os.path.join(basepath, 'static/images', f.filename), img)

        result['code'] = 0
        result['msg'] = 'success'
        result['data'] = {}
        result['data']['image_path'] = upload_path
        logger.info('result:{}'.format(result))
        return json.dumps(result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999, debug=True)
