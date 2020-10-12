import os
import cv2
from flask import Flask, request
import requests
import base64
import json
from BaiDuAi import BDAI_Face
from BaiDuAi import BDAI_Poem
import time
import logging
from flask import render_template

app = Flask(__name__, template_folder='templates', static_folder="static")

# static_image_url = '/home/ubuntu/HFAI/static/images'


@app.route("/index")
def hello_world():
    # print('hi')
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/api/bdai_face", methods=['POST'])
def baiDuAiFace():
    image_path = request.form['image_path']
    logging.info('image_path:{}'.format(image_path))
    small_image_path = str(image_path).split('.')[0] + '_' + str(
        time.time())[:8] + '_small.' + str(image_path).split('.')[1]
    logging.info('small_image_path:{}'.format(small_image_path))
    res = BDAI_Face(image_path)
    # logging.info('res:{}'.format(res))
    result = {}
    result["code"] = res["error_code"]  # 状态码
    result["msg"] = res["error_msg"]  # 消息
    if result["code"] == 0:
        result['data'] = {}
        result["data"]["face_num"] = res['result']["face_num"]  # 人脸数量
        # result["data"]["location"] = res['result']["face_list"][0][
        #     "location"]  # 人脸位置
        left = res['result']["face_list"][0]["location"]['left']  # 左
        top = res['result']["face_list"][0]["location"]['top']  # 上
        width = res['result']["face_list"][0]["location"]['width']  # 宽
        height = res['result']["face_list"][0]["location"]['height']  # 高
        h1 = int(top)
        h2 = int(top) + int(height)
        w1 = int(left)
        w2 = int(left) + int(width)
        bbox = [h1, h2, w1, w2]
        # 根据人脸位置获取小图并返回
        getSmallImage(image_path, small_image_path, bbox)
        result['data']['small_image_path'] = small_image_path
        result["data"]["age"] = res['result']["face_list"][0]["age"]  # 年龄
        result["data"]["beauty"] = res['result']["face_list"][0][
            "beauty"]  # 颜值
        brow = {'none': '不笑', 'smile': '微笑', 'laugh': '大笑'}
        result["data"]["expression"] = brow[res['result']["face_list"][0][
            "expression"]["type"]]  # 表情none:不笑；smile:微笑；laugh:大笑
        feature = {
            'square': '正方形',
            'triangle': '三角形',
            'oval': '椭圆',
            'heart': '心形',
            'round': '圆形'
        }
        result["data"]["face_shape"] = feature[
            res['result']["face_list"][0]["face_shape"]
            ["type"]]  # 脸型square: 正方形 triangle:三角形 oval: 椭圆 heart: 心形 round: 圆形
        gender = {'male': '男性', 'female': '女性'}
        result["data"]["gender"] = gender[res['result']["face_list"][0][
            "gender"]["type"]]  # male:男性 female:女性
        glasses = {'none': '无眼镜', 'common': '普通眼镜', 'sun': '墨镜'}
        result["data"]["glasses"] = glasses[res['result']["face_list"][0][
            "glasses"]["type"]]  # none:无眼镜，common:普通眼镜，sun:墨镜
        emotion = {
            'angry': '愤怒',
            'disgust': '厌恶',
            'fear': '恐惧',
            'happy': '高兴',
            'sad': '伤心',
            'surprise': '惊讶',
            'neutral': '无情绪'
        }
        result["data"]["emotion"] = emotion[
            res['result']["face_list"][0]["emotion"]
            ["type"]]  # 情绪angry:愤怒 disgust:厌恶 fear:恐惧 happy:高兴 sad: 伤心 surprise: 惊讶 neutral: 无情绪
        race = {
            'yellow': '黄种人',
            'white': '白种人',
            'black': '黑种人',
            'arabs': '阿拉伯人'
        }
        result["data"]["race"] = race[res['result']["face_list"][0]["race"][
            "type"]]  # 肤色yellow: 黄种人 white: 白种人 black:黑种人 arabs: 阿拉伯人
    logging.info('result:{}'.format(result))
    return json.dumps(result)


@app.route("/api/bdai_poem", methods=['POST'])
def baiDuAiPoem():
    word = request.form['text']
    logging.info('word:' + word)
    res = BDAI_Poem(word)
    return json.dumps(res)


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
    # x = bbox[0]
    # y = bbox[1]
    # cut = img[int(y):int(bbox[3]), int(x):int(bbox[2])]
    cut = img[bbox[0]:bbox[1], bbox[2]:bbox[3]]
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
        logging.info('filename:{}'.format(f.filename))
        # 处理上传图片位置
        filename = str(f.filename).split('.')[0] + '_' + str(
            time.time())[:8] + '.' + str(f.filename).split('.')[1]
        basepath = os.path.dirname(__file__)  # 当前文件所在路径
        upload_path = os.path.join(basepath, 'static/images',
                                   filename)  # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        f.save(upload_path)
        show_path = os.path.join('static/images', filename)
        logging.info('upload_path:{}'.format(upload_path))
        result['code'] = 0
        result['msg'] = 'success'
        result['data'] = {}
        result['data']['image_path'] = show_path
        # result['data']['image_path'] = upload_path
        # result['data']['show_path'] = show_path
        logging.info('result:{}'.format(result))
        return json.dumps(result)


if __name__ == "__main__":
    # logging.basicConfig(level=logging.INFO,
    #                     format='%(asctime)s %(filename)s(%(funcName)s)[line:%(lineno)d] %(levelname)s %(message)s',
    #                     datefmt='%a, %d %b %Y %H:%M:%S')
    logging.basicConfig(
        level=logging.INFO,
        format=
        '%(asctime)s %(filename)s(%(funcName)s)[line:%(lineno)d] %(levelname)s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S')
    app.run(host="0.0.0.0", port=9999, debug=True)
