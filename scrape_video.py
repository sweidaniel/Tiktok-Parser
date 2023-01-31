from selenium import webdriver #tool that allows automate tasks via a browser
import time
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen

#curl conversion of a tiktok link
def downloadVideo(link, id):
    cookies = {
        '__cflb': '02DiuEcwseaiqqyPC5qr2kcTPpjPMVimttMcHqwXhsmLP',
    }
    headers = {
        'authority': 'ssstik.io',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'cookie': '__cflb=02DiuEcwseaiqqyPC5qr2kcTPpjPMVimttMcHqwXhsmLP',
        'dnt': '1',
        'hx-current-url': 'https://ssstik.io/en',
        'hx-request': 'true',
        'hx-target': 'target',
        'hx-trigger': '_gcaptcha_pt',
        'origin': 'https://ssstik.io',
        'referer': 'https://ssstik.io/en',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    }
    params = {
        'url': 'dl',
    }
    data = {
        'id': link,
        'locale': 'en',
        'tt': 'WHJKd0cy',
    }

    response = requests.post('https://ssstik.io/abc', params=params, cookies=cookies, headers=headers, data=data)
    downloadSoup = BeautifulSoup(response.text, "html.parser")

    downloadLink = downloadSoup.a["href"]

    mp4File = urlopen(downloadLink)
    with open(f"videos/{id}.mp4", "wb") as output:
        while True:
            data = mp4File.read(4096)
            if data: 
                output.write(data)
            else:
                break

#driver gets our tiktok video link's html source
driver = webdriver.Chrome()
driver.get("https://www.tiktok.com/@papayaho.cat")

time.sleep(1)

#uses an online scroll app to get all videos on a certain page
scroll_pause_time = 1
screen_height = driver.execute_script("return window.screen.height;")
i = 1

while True:
    #scrolls one "height" at a time
    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
    i += 1
    time.sleep(scroll_pause_time)
    #update scroll height per pause
    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
    #break when we reach the end of the page 
    if (screen_height) * i > scroll_height:
        break

soup = BeautifulSoup(driver.page_source, "html.parser")
videos = soup.find_all("div", {"class": "tiktok-yz6ijl-DivWrapper"})

print(len(videos))
for index, video in enumerate(videos):
    downloadVideo(video.a["href"], index)
    #random number to make the host not think that we are a bot
    time.sleep(10) 
