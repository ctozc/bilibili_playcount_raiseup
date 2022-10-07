import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
from threading import Thread
import traceback


def get_proxy():
    return requests.get("http://127.0.0.1:5011/get").json()


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5011/delete/?proxy={}".format(proxy))


def change_time_type(str_time):
    m, s = str_time.split(':')
    return int(m) * 60 + int(s)


def play_one(url):
    retry_count = 5
    proxy = get_proxy().get("proxy")
    print("current proxy:" + proxy)
    delete_proxy(proxy)

    while retry_count > 0:
        try:
            # set proxy
            options = Options()
            options.add_argument(f"-proxy-server=http：//{proxy}")
            options.add_argument('--no-sandbox')
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            driver.get(url)

            time.sleep(5)

            # get video time
            video_time = driver.find_element(by=By.CLASS_NAME, value="bpx-player-ctrl-time-duration").text
            total_second = change_time_type(video_time)
            print("current video total second:", total_second)

            # click to play video
            # element = driver.find_element(By.XPATH, "//button[@class='bilibili-player-iconfont bilibili-player-iconfont-start']")
            # webdriver.ActionChains(driver).move_to_element(element).click(element).perform()

            driver.minimize_window()

            time.sleep(total_second + 5)
            return

        except Exception as e:
            traceback.print_exc()
            retry_count -= 1
        finally:
            # close page
            driver.close()
    return None


def always_play(url):
    while True:
        play_one(url)


if __name__ == '__main__':
    thread = 5
    get_proxy()
    url = ''
    play_one(url)
    thread_list = [Thread(target=always_play, args=(url,)) for _ in range(thread)]
    for t in thread_list:
        t.start()
        time.sleep(12)
