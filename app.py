import os

from flask import Flask
import requests
import base64
import json

from BaiDuAi import BDAI_Face, access_token

app = Flask(__name__)
static_image_url = '/home/ubuntu/HFAI/static/images'


@app.route("/")
def hello_world():
    # print('hi')
    return "欢迎来到我们的世界"


@app.route("/api/bdai")
def baiDuAi():
    res = BDAI_Face(os.path.join(static_image_url, "face.jpg"), access_token)
    result = {}
    result['data'] = {}
    result["error_code"] = res["error_code"]  # 状态码
    result["error_msg"] = res["error_msg"]  # 消息
    if res["error_code"] == 0:
        result["data"]["face_num"] = res['result']["face_num"]  # 人脸数量
        result["data"]["location"] = res['result']["face_list"][0][
            "location"]  # 人脸位置
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
    return result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9999, debug=True)
