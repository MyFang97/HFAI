import base64
import os

def getImgB64(imageUrl):
    """
    获取图片base64编码
    :param imageUrl: 图片路径
    :return:
    """
    # img_path = 'face.jpg'
    img = os.path.join('/home/ubuntu/HFAI', imageUrl)
    f_img = open(imageUrl, 'rb')  # 二进制方式打开图文件
    ls_f = base64.b64encode(f_img.read())  # 读取文件内容，转换为base64编码
    f_img.close()
    # print('ls_f:{}'.format(ls_f))
    return ls_f


# imgB64 = getImgB64()
