import base64

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

# imgB64 = getImgB64()
