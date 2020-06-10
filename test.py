
import time
import os
from selenium import webdriver
capture_screen_path = os.path.dirname(os.path.abspath(__file__))

def captureScreen(filename):
    print(capture_screen_path)
    browser = webdriver.Chrome(r"D:\\chromedriver")
    browser.set_window_size(1200, 900)
    browser.get("http://mail.126.com")  # Load page
    browser.execute_script("""
    (function () {
      var y = 0;
      var step = 100;
      window.scroll(0, 0);

      function f() {
        if (y < document.body.scrollHeight) {
          y += step;
          window.scroll(0, y);
          setTimeout(f, 50);
        } else {
          window.scroll(0, 0);
          document.title += "scroll-done";
        }
      }

      setTimeout(f, 1000);
    })();
  """)

    for i in range(30):
        if "scroll-done" in browser.title:
            break
        time.sleep(1)
    begin = time.time()
    for i in range(10):
        browser.save_screenshot(capture_screen_path+'/'+filename+str(begin)+".png")
    end = time.time()
    print(end - begin)
    return capture_screen_path+filename
    #browser.close()

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


takeScreenshot('xxx1')