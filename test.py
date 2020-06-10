
import time
import os
from selenium import webdriver
capture_screen_path = os.path.dirname(os.path.abspath(__file__))

projectPath = os.path.dirname(os.path.abspath(__file__))
screenRelativePath = "media/captureScreens/"

#
# def captureScreen(filename):
#     print(capture_screen_path)
#     browser = webdriver.Chrome(r"D:\\chromedriver")
#     browser.set_window_size(1200, 900)
#     browser.get("http://mail.126.com")  # Load page
#     browser.execute_script("""
#     (function () {
#       var y = 0;
#       var step = 100;
#       window.scroll(0, 0);
#
#       function f() {
#         if (y < document.body.scrollHeight) {
#           y += step;
#           window.scroll(0, y);
#           setTimeout(f, 50);
#         } else {
#           window.scroll(0, 0);
#           document.title += "scroll-done";
#         }
#       }
#
#       setTimeout(f, 1000);
#     })();
#   """)
#
#     for i in range(30):
#         if "scroll-done" in browser.title:
#             break
#         time.sleep(1)
#     begin = time.time()
#     for i in range(10):
#         browser.save_screenshot(capture_screen_path+'/'+filename+str(begin)+".png")
#     end = time.time()
#     print(end - begin)
#     return capture_screen_path+filename
#     #browser.close()

# captureScreen("xxx")


def takeScreenshot(filename):
    # picturePath = os.path.join(pictureName+'.png')
    browser = webdriver.Chrome(r"D:\\chromedriver")
    browser.set_window_size(1200, 900)
    browser.get("http://mail.126.com")  # Load page
    begin = time.time()
    try:
        browser.get_screenshot_as_file(filename+".png")
    except Exception  as e:
        print("error occurs: %s" % e)


def captureScreen(screenName):
    # 获取日期，如"2020-06-10"
    '''判断固定格式的日期是否存在，如"2019年\06月\10日"是否存在，如果不存在，新建一个，获取该路径，如果存在，则取该路径
        文件名格式：年月日时分秒+执行id+步骤id+".png"，如20200610224637-127-6.png
    '''

    print(projectPath)
    print(screenRelativePath)

    year, month, day = time.strftime("%Y-%m-%d").split("-")
    print(year, month,day)
    datePath = os.path.join(projectPath, screenRelativePath,"%s年"%year,"%s月"%month,"%s日"%day)
    print("datePath: %s" % datePath)
    print("os.path.exists(datePath): %s" % os.path.exists(datePath))
    if not os.path.exists(datePath):
        os.makedirs(datePath)
        print("os.path.exists(datePath): %s" % os.path.exists(datePath))
    # # os.makedirs()
    browser = webdriver.Chrome(r"D:\\chromedriver")
    browser.set_window_size(1200, 900)
    browser.get("http://mail.126.com")  # Load page
    picturePath = os.path.join(projectPath, screenRelativePath, datePath, screenName) + '.png'
    print("picturePath: %s" % picturePath)

    try:
        st =time.time()
        browser.get_screenshot_as_file(picturePath)
        et = time.time()
        print("total time: %s" %(et - st))
    except Exception  as e:
        print("error occurs: %s" % e)
    return os.path.join(screenRelativePath, screenName ) + '.png'

filename = time.strftime("%Y%m%d%H%M%S")

captureScreen(filename)