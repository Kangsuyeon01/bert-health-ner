import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup
import urllib.request as req
import argparse
import re
from urllib.parse import quote
import json
from tqdm import tqdm


def next_page(cnt):
    cnt += 1
    try:
        page = '//*[@id="content"]/div[2]/div[2]/span/a[{0}]'.format(cnt)
        next_btn = driver.find_element(By.XPATH, page)
        next_btn.click()
        return cnt
    except:
        return -1


def click_detail_page(num):  # 페이지 상세 클릭
    name_list = dict()
    while True:
        num += 1
        page = '//*[@id="listForm"]/div/div/ul/li[{0}]/div[2]/strong/a'.format(num)
        print(num)
        try:
            next_btn = driver.find_element(By.XPATH, page)
            name = next_btn.text
            name_list[name] = []
            next_btn.click()
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
                    title = '//*[@id="content"]/div[2]/div[1]/div[1]/ul/li/div[2]' # 부위, 질환 등에 관한 정보
                    context = '//*[@id="content"]/div[2]/div[1]'
                    # t_info = driver.find_element(By.XPATH, title)
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
    with open(savepath + 'data_anatomy.json', 'w', encoding="UTF-8") as f:
        json.dump(data, f, indent=4)


def readjson(savepath):
    with open(savepath + 'data_anatomy.json', 'r') as f:
        data = json.load(f)
    print(data)


if __name__ == "__main__":
    driver = webdriver.Chrome("chromedriver.exe")  # Path to where I installed the web driver

    driver.get(
        'https://www.amc.seoul.kr/asan/healthinfo/body/bodyList.do?partId=B000020')
    time.sleep(1)  # Let the user actually see something!

    data = {}
    for i in range(1,22):
        xpath = '//*[@id="diseaTab"]/div[1]/ul/li[{0}]/a'.format(i)
        word = driver.find_element(By.XPATH, xpath).text
        data[word] = explore_page(xpath)
        print(data[word])
        break


    # dict2json(data, './data/')
    # readjson('./data/')

