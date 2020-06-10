from PIL import Image, ImageDraw, ImageFont
import random
import string
import os


def create_captcha(width=100, height=40, fontSize=35):
    """
    width: 背景图片的宽度
    height:背景图片的高度
    fontsize：验证码的字体大小
    """
    img = Image.new("RGB", (width, height), getColor())  # 创建指定大小，背景颜色，模式的图片
    draw = ImageDraw.Draw(img)  # 创建画刷
    path = get_Font()  # 得到一个系统下的随机字体路径
    # 获取指定路径的字体
    font = ImageFont.truetype(font=path, size=fontSize)
    content = myrandom()  # 获取随机生成的验证码的值
    # 将验证码画到图片上
    draw.text((width * 0.1, height * 0.15), content, fill=getColor(), font=font)
    # 画干扰线
    for i in range(5):
        x = random.randint(0, 20)
        y = random.randint(0, height)
        z = random.randint(width - 20, width)
        w = random.randint(0, height)
        draw.line(((x, y), (z, w)), fill=getColor())
    # 返回验证码图片与文本内容
    return img, content


def getColor():
    # 随机生成一个元组类型的 RGB颜色
    color = (random.randint(0, 256), random.randint(0, 256), random.randint(0, 256))
    return color


def myrandom(count=5):
    myList = list(string.ascii_letters + string.digits)  # 指定要生成验证码的集合，数字，大小写字母
    # 在指定的mylist集合中随机取出count个集合
    lists = random.sample(myList, count)
    # 用指定的字符串连接集合中的内容
    return "".join(lists)


def get_Font(split='.ttf'):
    """返回操作系统下的指定后缀的字体"""
    if os.name == 'nt':
        path = 'C:\Windows\Fonts'.replace("\\", '/') + '/'
    else:
        # 根据不同的操作系统，系统字体在不同的文件下，Ubuntu下可以在/usr/share/fonts/ 下找到很多文件类型的字体
        path = '/usr/share/fonts/truetype/freefont/'
    listFont = os.listdir(path)
    # 获取指定后缀的字体，默认是.ttf类型的后缀
    fontList = [path + x for x in listFont if os.path.splitext(x)[1] == split]
    # 返回系统字体列表，以及所在的路径
    # return fontList, path
    # 随机返回一个字体
    path = random.sample(fontList, 1)
    return path[0]


img, content = create_captcha()
print("img: %s" % img)
print("content: %s" % content)