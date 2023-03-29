import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
import urllib.request as req
import argparse  # 특정 웹사이트로 접속하기 위해
import re
from urllib.parse import quote
import json
from tqdm import tqdm


def next_page(cnt):
    cnt += 1
    try:
        page = '//*[@id="gnrlzHealthInfoMainForm"]/div[4]/a[{0}]'.format(cnt)
        next_btn = driver.find_element(By.XPATH, page)
        next_btn.click()
        return cnt
    except:
        return -1


def click_detail_page(num):  # 페이지 상세 클릭
    name_list = dict()
    while True:
        num += 1
        page = '//*[@id="gnrlzHealthInfoMainForm"]/div[3]/ul/li[{0}]/a'.format(num)
        print(num)
        try:
            next_btn = driver.find_element(By.XPATH, page)
            name = next_btn.text
            name_list[name] = []
            next_btn.send_keys(Keys.CONTROL +"\n")
            taps = len(driver.window_handles)
            if taps > 1:
                # 새로운 탭으로 이동
                driver.switch_to.window(driver.window_handles[1])
                # url = driver.current_url  # 현재 url 가져오기
                # name_list[name].append(url)
                context = '/html/body'
                info = driver.find_element(By.XPATH, context)
                name_list[name].append(info.text)
                # 현재 사용중인 탭 종료
                driver.close()

                # 메인 탭으로 이동
                driver.switch_to.window(driver.window_handles[0])
            else:
                try:
                    context = '// *[ @ id = "print-content"]'
                    info = driver.find_element(By.XPATH, context)
                    name_list[name].append(info.text)
                except:
                    context = '/html/body'
                    info = driver.find_element(By.XPATH, context)
                    name_list[name].append(info.text)
                driver.back()
        except:
            print("Break!")
            break
    print(name_list)
    return name_list


def crawl_main(cnt):
    name_list = []
    num = 0
    while True:
        if cnt != -1:
            cnt = next_page(cnt)
            name_list.append(click_detail_page(num))
        else:
            break
    return cnt, name_list


def explore_page(xpath):
    cnt = 0
    total_name = []

    search_box = driver.find_element(By.XPATH, xpath)
    search_box.click()
    time.sleep(1)  # Let the user actually see something!

    while cnt != -1:
        cnt, name_list = crawl_main(cnt)
        total_name.append(name_list)

    return total_name


def dict2json(data, savepath):
    # json 파일로 저장
    with open(savepath + 'data_dis2.json', 'w', encoding="UTF-8") as f:
        json.dump(data, f, indent=4)


def readjson(savepath):
    with open(savepath + 'data_dis2.json', 'r') as f:
        data = json.load(f)
    print(data)


if __name__ == "__main__":
    driver = webdriver.Chrome("chromedriver.exe")  # Path to where I installed the web driver

    driver.get(
        'https://health.kdca.go.kr/healthinfo/biz/health/gnrlzHealthInfo/gnrlzHealthInfo/gnrlzHealthInfoMain.do?lclasSn=0')
    time.sleep(1)  # Let the user actually see something!

    data = {"질병": [], "건강": []}

    xpaths = ['//*[@id="gnrlzHealthInfoMainForm"]/div[2]/ul/li[2]/a',
              '//*[@id="gnrlzHealthInfoMainForm"]/div[2]/ul/li[3]/a']
    data['질병'] = explore_page(xpaths[0])
    # data['건강'] = explore_page(xpaths[1])

    dict2json(data, './data/')
    readjson('./data/')

