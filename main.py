import base64
import io
import json
import re
import time
import urllib.request

import requests
import requests
from bs4 import BeautifulSoup
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
from firebase_admin import storage
from PIL import Image
import os
import random
import openpyxl
import pandas as pd
from pyautogui import size
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import subprocess
import shutil
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import time
import datetime
import pyautogui
import pyperclip
import csv
import sys
import os
import math
import requests
import re
import random
import chromedriver_autoinstaller
from PyQt5.QtWidgets import QWidget, QApplication, QTreeView, QFileSystemModel, QVBoxLayout, QPushButton, QInputDialog, \
    QLineEdit, QMainWindow, QMessageBox, QFileDialog
from PyQt5.QtCore import QCoreApplication
from selenium.webdriver import ActionChains
import numpy
import datetime
from window import Ui_MainWindow
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import numpy as np
import pandas as pd
import os
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import DateRange
from google.analytics.data_v1beta.types import Dimension
from google.analytics.data_v1beta.types import Metric
from google.analytics.data_v1beta.types import RunReportRequest
from google.analytics.data_v1beta.types import OrderBy
import pprint
import boto3
import urllib3


def GetGangNam():
    print("지역 크롤링하기 시작")
    dataList = []
    regions = ['서울', '경기|인천', '대전|충청', '대구|경북', '부산|경남', '광주|전라', '강원도|제주']
    for region in regions:
        cookies = {
            'PHPSESSID': '4984k0pnhtiujtlof8d0981rv1',
            '_ga': 'GA1.1.451543972.1684079343',
            'hd_pops_15': '1',
            'e1192aefb64683cc97abb83c71057733': 'Y21w',
            '_ga_P9XZY1EJZ5': 'GS1.1.1684079343.1.1.1684079704.0.0.0',
        }

        headers = {
            'Accept': 'text/html, */*; q=0.01',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            # 'Cookie': 'PHPSESSID=4984k0pnhtiujtlof8d0981rv1; _ga=GA1.1.451543972.1684079343; hd_pops_15=1; e1192aefb64683cc97abb83c71057733=Y21w; _ga_P9XZY1EJZ5=GS1.1.1684079343.1.1.1684079704.0.0.0',
            'Referer': 'https://xn--939au0g4vj8sq.net/cp/?ca=20&loca_prt=%EC%84%9C%EC%9A%B8&local_1=%EC%A0%84%EC%B2%B4&local_2=%EC%84%9C%EC%9A%B8',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        params = {
            'ca': '20',
            'local_1': '전체',
            'local_2': region,
            'rpage': [
                '0',
                '0',
            ],
            'row_num': '5000',
        }

        response = requests.get(
            'https://xn--939au0g4vj8sq.net/theme/go/_list_cmp_tpl.php',
            params=params,
            cookies=cookies,
            headers=headers,
        )
        soup = BeautifulSoup(response.text, 'lxml')
        liTags = soup.find_all('li', attrs={'class': 'list_item'})
        for liTag in liTags:
            try:
                url = "https://xn--939au0g4vj8sq.net" + liTag.find('a')['href']
            except:
                url = ""
            # print('url:',url)

            # print(liTag)
            try:
                dday = liTag.find('span', attrs={'class': 'dday'}).get_text()
                regex = re.compile("\d+")
                dday = regex.findall(dday)[0]
            except:
                dday = "0"
            # print('dday:',dday)
            title = liTag.find('dt', attrs={'class': 'tit'}).get_text()
            # print('title:',title)
            status = liTag.find('span', attrs={'class': 'numb'}).get_text()
            regex = re.compile('신청 \d+')
            applyCount = regex.findall(status)[0].replace("신청", "")
            regex = re.compile('모집 \d+')
            demandCount = regex.findall(status)[0].replace("모집", "")
            # print('applyCount:',applyCount)
            # print('demandCount:',demandCount)
            if region == "강원|제주":
                region = "기타"
            try:
                imageUrl = liTag.find('img', attrs={'class': 'thumb_img'})['src']
                if imageUrl.find("https") < 0:
                    imageUrl = "https:" + imageUrl
            except:
                imageUrl = ""
            regex = re.compile("id=\d+")
            myIndex = regex.findall(url)[0].replace("id=", "")
            data = {'platform': '강남맛집', 'region': region, 'dday': dday, 'title': title, 'applyCount': applyCount,
                    'demandCount': demandCount, 'imageUrl': imageUrl, 'url': url, 'myImage': "강남맛집_" + myIndex}
            print(data)
            dataList.append(data)
        print("총갯수:", len(dataList))

    print("제품 크롤링하기 시작")
    cookies = {
        'PHPSESSID': '4984k0pnhtiujtlof8d0981rv1',
        '_ga': 'GA1.1.451543972.1684079343',
        'hd_pops_15': '1',
        'e1192aefb64683cc97abb83c71057733': 'Y21w',
        '_ga_P9XZY1EJZ5': 'GS1.1.1684079343.1.1.1684079704.0.0.0',
    }

    headers = {
        'Accept': 'text/html, */*; q=0.01',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        # 'Cookie': 'PHPSESSID=4984k0pnhtiujtlof8d0981rv1; _ga=GA1.1.451543972.1684079343; hd_pops_15=1; e1192aefb64683cc97abb83c71057733=Y21w; _ga_P9XZY1EJZ5=GS1.1.1684079343.1.1.1684079704.0.0.0',
        'Referer': 'https://xn--939au0g4vj8sq.net/cp/?ca=20&loca_prt=%EC%84%9C%EC%9A%B8&local_1=%EC%A0%84%EC%B2%B4&local_2=%EC%84%9C%EC%9A%B8',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    params = {
        'ca': '30',
        'rpage': [
            '0',
            '0',
        ],
        'row_num': '5000',
    }

    response = requests.get(
        'https://xn--939au0g4vj8sq.net/theme/go/_list_cmp_tpl.php',
        params=params,
        cookies=cookies,
        headers=headers,
    )
    soup = BeautifulSoup(response.text, 'lxml')
    liTags = soup.find_all('li', attrs={'class': 'list_item'})
    for liTag in liTags:
        try:
            url = "https://xn--939au0g4vj8sq.net" + liTag.find('a')['href']
        except:
            url = ""
        # print('url:',url)

        # print(liTag)
        try:
            dday = liTag.find('span', attrs={'class': 'dday'}).get_text()
            regex = re.compile("\d+")
            dday = regex.findall(dday)[0]
        except:
            dday = "0"
        # print('dday:',dday)
        title = liTag.find('dt', attrs={'class': 'tit'}).get_text()+"(배송형)"
        # print('title:',title)
        status = liTag.find('span', attrs={'class': 'numb'}).get_text()
        regex = re.compile('신청 \d+')
        applyCount = regex.findall(status)[0].replace("신청", "")
        regex = re.compile('모집 \d+')
        demandCount = regex.findall(status)[0].replace("모집", "")
        # print('applyCount:',applyCount)
        # print('demandCount:',demandCount)
        # if region=="강원|제주":
        #     region="기타"
        region = "기타"
        try:
            imageUrl = liTag.find('img', attrs={'class': 'thumb_img'})['src']
            if imageUrl.find("https") < 0:
                imageUrl = "https:" + imageUrl
        except:
            imageUrl = ""
        regex = re.compile("id=\d+")
        myIndex = regex.findall(url)[0].replace("id=", "")
        data = {'platform': '강남맛집', 'region': region, 'dday': dday, 'title': title, 'applyCount': applyCount,
                'demandCount': demandCount, 'imageUrl': imageUrl, 'url': url, 'myImage': "강남맛집_" + myIndex}
        print(data)
        dataList.append(data)
        print("총갯수:", len(dataList))

    return dataList


def GetNolowa():
    dataList = []
    print("지역크롤링시작")
    page = 1
    while True:
        cookies = {
            'PHPSESSID': 'sid67tsfqdbj2slve011j2bl73',
            '3dbe03ceb950cfecc3a0ba0538d4d0d6': 'MjExLjIxNS4xOTEuNzM%3D',
        }
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            # 'Cookie': 'PHPSESSID=sid67tsfqdbj2slve011j2bl73; 3dbe03ceb950cfecc3a0ba0538d4d0d6=MjExLjIxNS4xOTEuNzM%3D',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        params = {
            'category_id': '001',
            'sst': '',
            'sod': '',
            'page': str(page),
        }
        page = page + 1
        response = requests.get('https://www.cometoplay.kr/item_list.php', params=params, cookies=cookies,
                                headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        liGroup = soup.find('div', attrs={'class': 'item_box_list'})
        lis = liGroup.find_all('li')
        if len(lis) == 0:
            break
        for li in lis:
            url = 'https://www.cometoplay.kr/' + li.find('a')['href']
            title = li.find('span', attrs={'class': 'it_name'}).get_text()
            # print('title:',title)
            dday = li.find('span', attrs={'class': 'txt_num'}).get_text()
            regex = re.compile("\d+")
            dday = regex.findall(dday)[0]
            # print('dday:',dday)
            applyCount = li.find('b', attrs={'class': 'txt_num point_color4'}).get_text()
            # print('applyCount:',applyCount)
            demandCount = li.find('b', attrs={'style': 'color:#666;'}).get_text()
            # print('demandCount:',demandCount)
            imageUrl = li.find('img')['src'].replace('./', 'https://cometoplay.kr/')
            # print('imageUrl:',imageUrl)

            region = "기타"
            if title.find('서울') >= 0:
                region = "서울"
            elif title.find('경기') >= 0 or title.find('인천') >= 0:
                region = "경기|인천"
            elif title.find('대전') >= 0 or title.find('충남') >= 0 or title.find('충청') >= 0 or title.find('충북') >= 0:
                region = "대전|충청"
            elif title.find('대구') >= 0 or title.find('경북') >= 0:
                region = "대전|충청"
            elif title.find('부산') >= 0 or title.find('경남') >= 0:
                region = "부산|경남"
            elif title.find('광주') >= 0 or title.find('전남') >= 0 or title.find('전북') >= 0:
                region = "광주|전라"

            regex = re.compile("it_id=\d+")
            myIndex = regex.findall(url)[0].replace("it_id=", "")

            data = {'platform': '놀러와체험단', 'region': region, 'dday': dday, 'title': title, 'applyCount': applyCount,
                    'demandCount': demandCount, 'imageUrl': imageUrl, 'url': url, 'myImage': "놀러와체험단_" + myIndex}
            print(data)
            dataList.append(data)
        time.sleep(0.5)
        print("총갯수:", len(dataList))

    print("제품크롤링시작")
    page = 1
    while True:
        cookies = {
            'PHPSESSID': 'sid67tsfqdbj2slve011j2bl73',
            '3dbe03ceb950cfecc3a0ba0538d4d0d6': 'MjExLjIxNS4xOTEuNzM%3D',
        }
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            # 'Cookie': 'PHPSESSID=sid67tsfqdbj2slve011j2bl73; 3dbe03ceb950cfecc3a0ba0538d4d0d6=MjExLjIxNS4xOTEuNzM%3D',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        params = {
            'category_id': '002',
            'sst': '',
            'sod': '',
            'page': str(page),
        }
        page = page + 1
        response = requests.get('https://www.cometoplay.kr/item_list.php', params=params, cookies=cookies,
                                headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        liGroup = soup.find('div', attrs={'class': 'item_box_list'})
        lis = liGroup.find_all('li')
        if len(lis) == 0:
            break
        for li in lis:
            url = 'https://www.cometoplay.kr/' + li.find('a')['href']
            title = li.find('span', attrs={'class': 'it_name'}).get_text()+"(배송형)"
            # print('title:',title)
            dday = li.find('span', attrs={'class': 'txt_num'}).get_text()
            regex = re.compile("\d+")
            dday = regex.findall(dday)[0]
            # print('dday:',dday)
            applyCount = li.find('b', attrs={'class': 'txt_num point_color4'}).get_text()
            # print('applyCount:',applyCount)
            demandCount = li.find('b', attrs={'style': 'color:#666;'}).get_text()
            # print('demandCount:',demandCount)
            imageUrl = li.find('img')['src'].replace('./', 'https://cometoplay.kr/')
            # print('imageUrl:',imageUrl)

            region = "기타"
            # if title.find('서울') >= 0:
            #     region = "서울"
            # elif title.find('경기') >= 0 or title.find('인천') >= 0:
            #     region = "경기|인천"
            # elif title.find('대전') >= 0 or title.find('충남') >= 0 or title.find('충청') >= 0 or title.find('충북') >= 0:
            #     region = "대전|충청"
            # elif title.find('대구') >= 0 or title.find('경북') >= 0:
            #     region = "대전|충청"
            # elif title.find('부산') >= 0 or title.find('경남') >= 0:
            #     region = "부산|경남"
            # elif title.find('광주') >= 0 or title.find('전남') >= 0 or title.find('전북') >= 0:
            #     region = "광주|전라"

            regex = re.compile("it_id=\d+")
            myIndex = regex.findall(url)[0].replace("it_id=", "")

            data = {'platform': '놀러와체험단', 'region': region, 'dday': dday, 'title': title, 'applyCount': applyCount,
                    'demandCount': demandCount, 'imageUrl': imageUrl, 'url': url, 'myImage': "놀러와체험단_" + myIndex}
            print(data)
            dataList.append(data)
        time.sleep(0.5)
        print("총갯수:", len(dataList))
    return dataList


def GetDinnerQueen():
    dataList = []

    page = 1
    while True:
        cookies = {
            '_fbp': 'fb.1.1684080159081.1105236955',
            'PHPSESSID': '6e5437bafc8baedfdf62265e589e761a311dce4c',
            '_gid': 'GA1.2.1430089283.1684244645',
            '_gat_UA-58677533-2': '1',
            'wcs_bt': 'unknown:1684245532',
            '_ga_GFE876V0LZ': 'GS1.1.1684244621.3.1.1684245532.0.0.0',
            '_ga': 'GA1.1.668113333.1684080158',
        }

        headers = {
            'authority': 'dinnerqueen.net',
            'accept': '*/*',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            # 'content-length': '0',
            # 'cookie': '_fbp=fb.1.1684080159081.1105236955; PHPSESSID=6e5437bafc8baedfdf62265e589e761a311dce4c; _gid=GA1.2.1430089283.1684244645; _gat_UA-58677533-2=1; wcs_bt=unknown:1684245532; _ga_GFE876V0LZ=GS1.1.1684244621.3.1.1684245532.0.0.0; _ga=GA1.1.668113333.1684080158',
            'origin': 'https://dinnerqueen.net',
            'referer': 'https://dinnerqueen.net/taste?ct=%EC%A7%80%EC%97%AD&lpage=3&query=&deal=&cate=&order=&area1=%EC%A0%84%EA%B5%AD&area2=%EC%A0%84%EC%B2%B4',
            'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        params = {
            'ct': '지역',
            'area1': '전국',
            'area2': '전체',
            'page': str(page),
            'query': '',
        }
        page = page + 1
        response = requests.post('https://dinnerqueen.net/taste/taste_list', params=params, cookies=cookies,
                                 headers=headers)
        try:
            result = json.loads(response.text)['layout']
        except:
            break
        soup = BeautifulSoup(result, 'lxml')
        allTags = soup.find_all('div', attrs={'class': 'qz-col pc2 lt3 tb2 mb2 mr-b8 mb-mr-b6'})
        isAllTags = len(allTags)
        if isAllTags == 0:
            break
        for eachtag in allTags:
            url = 'https://dinnerqueen.net' + eachtag.find('a')['href']

            title = eachtag.find('p', attrs={'class': 'qz-body-kr mb-qz-body2-kr ellipsis-2 color-title'}).get_text().replace("\n","").strip()
            # print('title:',title)
            try:
                dday = eachtag.find('p', attrs={'class': 'qz-badge m layer-primary mr-b1 ver-t'}).get_text()
                dday = dday.replace("일 남음", "").strip()
            except:
                dday = 0
            # print('dday:',dday)
            applyCount = 0
            demandCount = 0
            imageUrl = eachtag.find('img')['src']
            # print('imageUrl:',imageUrl)
            isBaesong=False
            try:
                baesong=eachtag.find('strong',attrs={'class':'keep-a'}).get_text()
                if baesong.find("배송형")>=0:
                    isBaesong=True
            except:
                baesong=""
            print("isBaesong:",isBaesong,"/ isBaesong_TYPE:",type(isBaesong))

            if isBaesong==True:
                title=title+"(배송형)"

            region = "기타"
            if title.find('서울') >= 0:
                region = "서울"
            elif title.find('경기') >= 0 or title.find('인천') >= 0:
                region = "경기|인천"
            elif title.find('대전') >= 0 or title.find('충남') >= 0 or title.find('충청') >= 0 or title.find('충북') >= 0:
                region = "대전|충청"
            elif title.find('대구') >= 0 or title.find('경북') >= 0:
                region = "대전|충청"
            elif title.find('부산') >= 0 or title.find('경남') >= 0:
                region = "부산|경남"
            elif title.find('광주') >= 0 or title.find('전남') >= 0 or title.find('전북') >= 0:
                region = "광주|전라"

            regex = re.compile("/\d+")
            myIndex = regex.findall(url)[0].replace("/", "")

            data = {'platform': '디너의여왕', 'region': region, 'dday': dday, 'title': title, 'applyCount': applyCount,
                    'demandCount': demandCount, 'imageUrl': imageUrl, 'url': url, 'myImage': "디너의여왕_" + myIndex}
            print(data)
            dataList.append(data)
        print("총갯수:", len(dataList))
        time.sleep(0.5)
    return dataList


def GetDailyView():
    print("지역크롤링")
    dataList = []
    page = 1
    while True:
        cookies = {
            'PHPSESSID': 'pq5but4qs6umog2cqtr2o4hci5',
            '3dbe03ceb950cfecc3a0ba0538d4d0d6': 'MjExLjIxNS4xOTEuNzM%3D',
        }

        headers = {
            'authority': 'www.dailyview.kr',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            # 'cookie': 'PHPSESSID=pq5but4qs6umog2cqtr2o4hci5; 3dbe03ceb950cfecc3a0ba0538d4d0d6=MjExLjIxNS4xOTEuNzM%3D',
            'referer': 'https://www.dailyview.kr/item_list.php?category_id=001',
            'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        }

        params = {
            'category_id': '001',
            'sst': '',
            'sod': '',
            'page': str(page),
        }
        page = page + 1
        response = requests.get('https://www.dailyview.kr/item_list.php', params=params, cookies=cookies,
                                headers=headers)

        soup = BeautifulSoup(response.text, 'lxml')
        liGroup = soup.find('div', attrs={'class': 'item_box_list'})
        lis = liGroup.find_all('li')
        if len(lis) == 0:
            break
        for li in lis:
            url = 'https://dailyview.kr/' + li.find('a')['href']
            title = li.find('span', attrs={'class': 'it_name'}).get_text()
            # print('title:',title)
            dday = li.find('span', attrs={'class': 'txt_num'}).get_text()
            regex = re.compile("\d+")
            dday = regex.findall(dday)[0]
            # print('dday:',dday)
            applyCount = li.find('b', attrs={'class': 'txt_num point_color4'}).get_text()
            # print('applyCount:',applyCount)
            demandCount = li.find('b', attrs={'style': 'color:#666;'}).get_text()
            # print('demandCount:',demandCount)
            imageUrl = li.find('img')['src'].replace('./', 'https://dailyview.kr/')
            # print('imageUrl:',imageUrl)

            region = "기타"
            if title.find('서울') >= 0:
                region = "서울"
            elif title.find('경기') >= 0 or title.find('인천') >= 0:
                region = "경기|인천"
            elif title.find('대전') >= 0 or title.find('충남') >= 0 or title.find('충청') >= 0 or title.find('충북') >= 0:
                region = "대전|충청"
            elif title.find('대구') >= 0 or title.find('경북') >= 0:
                region = "대전|충청"
            elif title.find('부산') >= 0 or title.find('경남') >= 0:
                region = "부산|경남"
            elif title.find('광주') >= 0 or title.find('전남') >= 0 or title.find('전북') >= 0:
                region = "광주|전라"
            regex = re.compile("it_id=\d+")
            myIndex = regex.findall(url)[0].replace("it_id=", "")

            data = {'platform': '데일리뷰', 'region': region, 'dday': dday, 'title': title, 'applyCount': applyCount,
                    'demandCount': demandCount, 'imageUrl': imageUrl, 'url': url, 'myImage': "데일리뷰_" + myIndex}
            print(data)
            dataList.append(data)
        time.sleep(0.5)
        print("총갯수:", len(dataList))

    print("제품크롤링")
    page = 1
    while True:
        cookies = {
            'PHPSESSID': 'pq5but4qs6umog2cqtr2o4hci5',
            '3dbe03ceb950cfecc3a0ba0538d4d0d6': 'MjExLjIxNS4xOTEuNzM%3D',
        }

        headers = {
            'authority': 'www.dailyview.kr',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            # 'cookie': 'PHPSESSID=pq5but4qs6umog2cqtr2o4hci5; 3dbe03ceb950cfecc3a0ba0538d4d0d6=MjExLjIxNS4xOTEuNzM%3D',
            'referer': 'https://www.dailyview.kr/item_list.php?category_id=001',
            'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
        }

        params = {
            'category_id': '002',
            'sst': '',
            'sod': '',
            'page': str(page),
        }
        page = page + 1
        response = requests.get('https://www.dailyview.kr/item_list.php', params=params, cookies=cookies,
                                headers=headers)

        soup = BeautifulSoup(response.text, 'lxml')
        liGroup = soup.find('div', attrs={'class': 'item_box_list'})
        lis = liGroup.find_all('li')
        if len(lis) == 0:
            break
        for li in lis:
            url = 'https://dailyview.kr/' + li.find('a')['href']
            title = li.find('span', attrs={'class': 'it_name'}).get_text()+"(배송형)"
            # print('title:',title)
            dday = li.find('span', attrs={'class': 'txt_num'}).get_text()
            regex = re.compile("\d+")
            dday = regex.findall(dday)[0]
            # print('dday:',dday)
            applyCount = li.find('b', attrs={'class': 'txt_num point_color4'}).get_text()
            # print('applyCount:',applyCount)
            demandCount = li.find('b', attrs={'style': 'color:#666;'}).get_text()
            # print('demandCount:',demandCount)
            imageUrl = li.find('img')['src'].replace('./', 'https://dailyview.kr/')
            # print('imageUrl:',imageUrl)

            region = "기타"
            if title.find('서울') >= 0:
                region = "서울"
            elif title.find('경기') >= 0 or title.find('인천') >= 0:
                region = "경기|인천"
            elif title.find('대전') >= 0 or title.find('충남') >= 0 or title.find('충청') >= 0 or title.find('충북') >= 0:
                region = "대전|충청"
            elif title.find('대구') >= 0 or title.find('경북') >= 0:
                region = "대전|충청"
            elif title.find('부산') >= 0 or title.find('경남') >= 0:
                region = "부산|경남"
            elif title.find('광주') >= 0 or title.find('전남') >= 0 or title.find('전북') >= 0:
                region = "광주|전라"
            regex = re.compile("it_id=\d+")
            myIndex = regex.findall(url)[0].replace("it_id=", "")

            data = {'platform': '데일리뷰', 'region': region, 'dday': dday, 'title': title, 'applyCount': applyCount,
                    'demandCount': demandCount, 'imageUrl': imageUrl, 'url': url, 'myImage': "데일리뷰_" + myIndex}
            print(data)
            dataList.append(data)
        time.sleep(0.5)
        print("총갯수:", len(dataList))

    return dataList


def GetGaBoJa():
    dataList = []
    count = 1
    endFlag = False
    while True:
        cookies = {
            'PHPSESSID': 'o9tk6tr5lrjvnmdb5s452oq79r',
            '2a0d2363701f23f8a75028924a3af643': 'MjExLjIxNS4xOTEuNzM%3D',
            'ch-veil-id': '7994c59a-98a7-4143-a5ea-4784c21c1036',
            '5b1ceb69146c0bafdc082ff42248da98': 'MTY4Njg4NDk1MQ%3D%3D',
            'ch-session-87071': 'eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJzZXMiLCJrZXkiOiI4NzA3MS02NDhkYjQ5NzA2ZGI3NzFiMmMxYSIsImlhdCI6MTY4NzAwODgyNywiZXhwIjoxNjg5NjAwODI3fQ.OslCUitKkUCAsFnilLrV7U86aEwQ58MfwO8boq26j9I',
        }

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            # 'Cookie': 'PHPSESSID=o9tk6tr5lrjvnmdb5s452oq79r; 2a0d2363701f23f8a75028924a3af643=MjExLjIxNS4xOTEuNzM%3D; ch-veil-id=7994c59a-98a7-4143-a5ea-4784c21c1036; 5b1ceb69146c0bafdc082ff42248da98=MTY4Njg4NDk1MQ%3D%3D; ch-session-87071=eyJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJzZXMiLCJrZXkiOiI4NzA3MS02NDhkYjQ5NzA2ZGI3NzFiMmMxYSIsImlhdCI6MTY4NzAwODgyNywiZXhwIjoxNjg5NjAwODI3fQ.OslCUitKkUCAsFnilLrV7U86aEwQ58MfwO8boq26j9I',
            'Referer': 'http://xn--o39a04kpnjo4k9hgflp.com/shop/search.php',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
        }

        params = {
            'page': str(count),
            'q': '',
            'chennel[]': '',
            'ca_kind[]': '',
            'ar_code1': '',
        }

        response = requests.get(
            'http://xn--o39a04kpnjo4k9hgflp.com/shop/ajax.campaign_list.php',
            params=params,
            cookies=cookies,
            headers=headers,
            verify=False,
        )
        response.raise_for_status()
        try:
            results = json.loads(response.text)['items']
        except:
            print("상품없는듯")
        if len(results) == 0:
            break
        # pprint.pprint(results)

        for result in results:
            # pprint.pprint(result)
            title = result['ca_info3']
            # print(title)
            applyCount = result['apply_cnt']
            # print(applyCount)
            region = ""
            dday = result['deadline_days']
            demandCount = result['ca_creator_cnt']
            try:
                imageUrl = result['thumb'].split('"')[1]
            except:
                imageUrl = ""
            # print(imageUrl)
            url = 'http://xn--o39a04kpnjo4k9hgflp.com' + result['href']
            regex = re.compile("\d+")
            myIndex = regex.findall(url)[-1]
            try:
                endDate = result['ca_edate']
                print(endDate)
                endDateTimestamp = datetime.datetime.strptime(endDate, '%Y-%m-%d').timestamp()
            except:
                print("날짜에러")
                continue

            if endDateTimestamp < datetime.datetime.now().timestamp():
                print("과거 것은 크롤링 중지")
                endFlag = True
                break
            data = {'platform': '가보자체험단', 'region': region, 'dday': dday, 'title': title, 'applyCount': applyCount,
                    'demandCount': demandCount, 'imageUrl': imageUrl, 'url': url, 'myImage': "가보자체험단_" + myIndex}
            print(data)
            dataList.append(data)
        if endFlag == True:
            print("과거 것은 크롤링 중지2")
            break
        print(endDate)
        print(count, "번째 페이지 크롤링 완료")
        count += 1
        time.sleep(0.5)
    return dataList


def GetMrBlog():
    categorys = ['지역', '제품', 'instagram']
    dataList = []
    for category in categorys:
        count = 1
        while True:
            cookies = {
                'ci_session': '8ccf93e08f066efbaff070256584be25ed7f55e4',
                '_ga': 'GA1.1.1856735572.1687012136',
                '_ga_D3DEYJM5M9': 'GS1.1.1687012135.1.1.1687012181.0.0.0',
            }

            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                'Connection': 'keep-alive',
                # 'Cookie': 'ci_session=8ccf93e08f066efbaff070256584be25ed7f55e4; _ga=GA1.1.1856735572.1687012136; _ga_D3DEYJM5M9=GS1.1.1687012135.1.1.1687012181.0.0.0',
                'Referer': 'http://www.mrblog.net/campaign/campaignList/%EC%A7%80%EC%97%AD',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest',
            }

            params = {
                'page': str(count),
                'menuCategory': '',
                'areaBigCategory': '',
                'areaMidCategory': '',
            }

            response = requests.get(
                'http://www.mrblog.net/api/campaigns/{}'.format(category),
                params=params,
                cookies=cookies,
                headers=headers,
                verify=False,
            )
            response.raise_for_status()

            try:
                results = json.loads(response.text)
            except:
                print('상품없음')
                break
            if len(results) == 0:
                print('상품없음')
                break
            # pprint.pprint(result)
            for result in results:


                title = result['title']
                if category == "제품":
                    title=title+"(배송형)"
                region = ""
                dday = result['day']
                imageUrl = result['image']
                url = 'http://www.mrblog.net/campaign/campaignViewIndex/' + result['pk']
                applyCount = result['joinCount']
                demandCount = result['max_number_of_people']
                myIndex = result['pk']

                data = {'platform': '미블', 'region': region, 'dday': dday, 'title': title, 'applyCount': applyCount,
                        'demandCount': demandCount, 'imageUrl': imageUrl, 'url': url, 'myImage': "미블_" + myIndex}
                print(data)
                dataList.append(data)
                # dataList.append(data)
            print(category, '/', count, "번째 페이지 크롤링 완료..")
            count = count + 1
            time.sleep(0.5)
    return dataList


def GetOhMyBlog():
    dataList = []
    categoryTypeList = ['C', 'D']
    for categoryType in categoryTypeList:
        count = 1
        while True:
            cookies = {
                'ASP.NET_SessionId': 'e5f5f1rzi3y4ldr5r1twdihv',
            }

            headers = {
                'authority': 'kormedia.co.kr',
                'accept': 'text/html, */*; q=0.01',
                'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                # 'cookie': 'ASP.NET_SessionId=e5f5f1rzi3y4ldr5r1twdihv',
                'referer': 'https://kormedia.co.kr/Recruitment/list?p_cateType=C&p_country_seq=0&p_country_group_seq=0&pageNum=0',
                'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
            }

            params = {
                'p_cateType': str(categoryType),
                'p_country_seq': '0',
                'p_country_group_seq': '0',
                'pageNum': str(count),
                'searchText': '',
                'isBackDataLoad': 'false',
            }
            try:
                response = requests.get('https://kormedia.co.kr/recruitment/searchList', params=params, cookies=cookies,
                                        headers=headers)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'lxml')
                # pprint.pprint(soup.prettify())
                products = soup.find_all('div', attrs={'class': 'content_box'})
                print("상품수는:", len(products))
            except:
                break
            if len(products) == 0:
                break
            for product in products:
                title = product.find('div', attrs={'class': 'omb_text_box'}).get_text().strip()
                if categoryType=="D":
                    title=title+"(배송형)"
                region = ""
                dday = product.find('div', attrs={'class': 'text_box_day_text'}).get_text().strip().replace("D-", "")
                # print(dday)
                applyCount = ""
                demandCount = product.find('div', attrs={'class': 'omb_people'}).get_text().replace("명모집", "").strip()
                imageUrl = product.find('img')['src']
                url = 'https://kormedia.co.kr/Recruitment/InformationAll?p_app_seq=' + \
                      product.find('div', attrs={'class': 'scrap_box'})['data-appseq']
                myIndex = product.find('div', attrs={'class': 'scrap_box'})['data-appseq']

                data = {'platform': '오마이블로그', 'region': region, 'dday': dday, 'title': title, 'applyCount': applyCount,
                        'demandCount': demandCount, 'imageUrl': imageUrl, 'url': url, 'myImage': "오마이블로그_" + myIndex}
                print(data)
                dataList.append(data)
            print(count, "번째 페이지 완료, 상품수:", len(dataList))
            count += 1
            time.sleep(random.randint(5, 10) * 0.1)
    return dataList


def GetSeoulObba():
    dataList = []
    categorys = ['377', '383']  #
    for category in categorys:
        endFlag = False
        print("카테고리는:", category)
        count = 1
        while True:
            if count == 1:
                import requests

                cookies = {
                    'PHPSESSID': 'aulpu7p53dhgaa35mp99nnej85',
                    '_gid': 'GA1.3.1254424238.1687227741',
                    '_ga_R6W40510YH': 'GS1.1.1687242330.3.1.1687244529.0.0.0',
                    '_ga': 'GA1.3.1785828696.1687011897',
                }

                headers = {
                    'authority': 'www.seoulouba.co.kr',
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                    # 'cookie': 'PHPSESSID=aulpu7p53dhgaa35mp99nnej85; _gid=GA1.3.1254424238.1687227741; _ga_R6W40510YH=GS1.1.1687242330.3.1.1687244529.0.0.0; _ga=GA1.3.1785828696.1687011897',
                    'if-modified-since': 'Tue, 20 Jun 2023 06:49:05 GMT',
                    'referer': 'https://www.seoulouba.co.kr/campaign/?cat=383',
                    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                }

                response = requests.get(
                    f'https://www.seoulouba.co.kr/campaign/?cat={category}&qq=&q=&q1=&q2=&ar1=&ar2=&&sort=deadline',
                    cookies=cookies,
                    headers=headers,
                )
            else:
                cookies = {
                    'PHPSESSID': 'aulpu7p53dhgaa35mp99nnej85',
                    '_gid': 'GA1.3.1254424238.1687227741',
                    '_gat_gtag_UA_232975080_1': '1',
                    '_ga_R6W40510YH': 'GS1.1.1687227740.2.1.1687227763.0.0.0',
                    '_ga': 'GA1.3.1785828696.1687011897',
                }

                headers = {
                    'authority': 'www.seoulouba.co.kr',
                    'accept': '*/*',
                    'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                    # 'cookie': 'PHPSESSID=aulpu7p53dhgaa35mp99nnej85; _gid=GA1.3.1254424238.1687227741; _gat_gtag_UA_232975080_1=1; _ga_R6W40510YH=GS1.1.1687227740.2.1.1687227763.0.0.0; _ga=GA1.3.1785828696.1687011897',
                    'origin': 'https://www.seoulouba.co.kr',
                    'referer': 'https://www.seoulouba.co.kr/campaign/?cat=377',
                    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'empty',
                    'sec-fetch-mode': 'cors',
                    'sec-fetch-site': 'same-origin',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                    'x-requested-with': 'XMLHttpRequest',
                }

                moreContant = 156

                data = {
                    'cat': category,
                    'qq': '',
                    'q': '',
                    'q1': '',
                    'q2': '',
                    'ar1': '',
                    'ar2': '',
                    'sort': 'deadline',
                    'page': str(count),
                    # 'more': str(36*(count-1)+moreContant),
                    'rows': '1000',
                }

                response = requests.post('https://www.seoulouba.co.kr/campaign/ajax/list.ajax.php', cookies=cookies,
                                         headers=headers, data=data)
                response.raise_for_status()
            try:
                soup = BeautifulSoup(response.text, 'lxml')
                # print(soup.prettify())
                products = soup.find_all('li', attrs={'class': 'campaign_content'})
                if len(products) == 0:
                    print("더없음")
                    break
            except:
                print('더없음')
                break

            for product in products:
                title = product.find('strong', attrs={'class': 's_campaign_title'}).get_text().strip()
                if category=="383":
                    title=title+"(배송형)"
                region = ""
                dday = product.find('div', attrs={'class': 'd_day'}).get_text().replace("D-", "").strip()
                if dday == "day":
                    dday = 0
                # if dday=="마감":
                #     continue
                # print(title,count,dday)
                CountRaw = product.find('div', attrs={'class': 'recruit'}).get_text()
                regex1 = re.compile("신청 \d+")
                regex2 = re.compile("모집 \d+")
                applyCount = regex1.findall(CountRaw)[0].replace("신청", "").strip()
                demandCount = regex2.findall(CountRaw)[0].replace("모집", "").strip()
                imageUrl = product.find('img')['src']
                url = product.find('a', attrs={'class': 'tum_img'})['href']
                regex3 = re.compile("\d+")
                myIndex = regex3.findall(url)[0]

                if dday == "마감":
                    print("마감됨")
                    endFlag = True
                    break
                data = {'platform': '서울오빠', 'region': region, 'dday': dday, 'title': title, 'applyCount': applyCount,
                        'demandCount': demandCount, 'imageUrl': imageUrl, 'url': url, 'myImage': "서울오빠_" + myIndex}
                print(data)
                dataList.append(data)
            print("상품수는:", len(dataList))
            if endFlag == True:
                break
            count += 1
            time.sleep(random.randint(5, 10) * 0.1)
    return dataList


def GetRevu():
    categorys = ['제품', '지역']
    dataList = []
    for category in categorys:
        count = 1
        while True:
            headers = {
                'authority': 'api.weble.net',
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                'origin': 'https://www.revu.net',
                'referer': 'https://www.revu.net/',
                'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'cross-site',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            }

            params = {
                'cat': str(category),
                'limit': '100',
                'media[]': [
                    'blog',
                    'instagram',
                    'youtube',
                ],
                'page': str(count),
                'sort': 'latest',
                'type': 'play',
            }

            try:
                response = requests.get('https://api.weble.net/v1/campaigns', params=params, headers=headers)
                response.raise_for_status()
                results = json.loads(response.text)['items']
            except:
                print("더없음2")
                break
            if len(results) == 0:
                print("더없음")
                break

            for result in results:

                title = result['item']
                if category=="제품":
                    title=title+"(배송형)"
                # print(title)
                region = ""
                dday = result['byDeadline']
                if dday==0:
                    print("당일은건너뜀")
                    continue

                applyCount = result['campaignStats']['requestCount']
                demandCount = result['reviewerLimit']
                imageUrl = result['thumbnail']
                url = 'https://www.revu.net/campaign/' + str(result['id'])
                myIndex = str(result['id'])
                data = {'platform': '레뷰', 'region': region, 'dday': dday, 'title': title, 'applyCount': applyCount,
                        'demandCount': demandCount, 'imageUrl': imageUrl, 'url': url, 'myImage': "레뷰_" + myIndex}
                print(data)
                dataList.append(data)
            print("데이타갯수:", len(dataList))
            count += 1
            time.sleep(random.randint(5, 10) * 0.1)
    return dataList


def SaveFirebaseDB(totalList):
    db = firebase_admin.db
    ref = db.reference()  # db 위치 지정, 기본 가장 상단을 가르킴
    ref.update({"data": totalList})
    print("저장완료")


def SaveFirebaseVisitors(totalList):
    db = firebase_admin.db
    ref = db.reference()  # db 위치 지정, 기본 가장 상단을 가르킴
    ref.update({"visitors": totalList})
    print("저장완료")


def SaveFirebaseRegiToken(regiToken):
    db = firebase_admin.db
    ref = db.reference()  # db 위치 지정, 기본 가장 상단을 가르킴
    ref.update({"regiToken": regiToken})
    print("저장완료")


def InitFirebase():
    cred = credentials.Certificate({
        "type": "service_account",
        "project_id": "experience-gen",
        "private_key_id": "6a967ec5eea30528f569dea9a04f3d136a6375cd",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC5gcn0Igb0HlUH\nF3af6eFWdJmynoUxJUVfBloJ/UUCWn4zLQUuUfd8r04L/wTYrV4CKcORJfl85T2/\nxSupVctXpg0Bzu4vDOB7eUEE7F68TSZVRKCMnimOft2QMlwljPbkG65dCJEMKRXL\nLb68oQ8Ko8epWkf5dWpnsrugajvRHriaoMXv6e8gVrZTCM4ShoJTqRZhot+u1goL\n8kRZuiS4nugZ/ezzWLVYMMaUYFavOkVvWcFvv4hmyu8FnmXGNi0hkGGWh8iLv7KH\n1keSdvcZVDk/mhqMKsz8e3gZazF1ovYYvdIOni8bdwB9YHJZo41pangWEXMglI8S\nZZ46IFf9AgMBAAECggEAEXvFWDhUxhvjEPYJ0hcti65q8JthcOOoXsUEe2iJYSgS\nONSHZnmHL73TR0IpEhrU1LNcS95zsxe6nXZXH8XcPPiDb/uGwJx1aRhhI7ZQqhfu\nAvSi2l3rC2kIN2zno7UIwoWcBgdRVFS9nxaX9sM0iGDYkoIrF7xp441u2Dbq8vx0\nbUAdj5mJEVvaOAtzr55EARxPEqL6zUttoHRzJ4pnTUKuVsJ69sibqua0pmwCurlF\n3PWNgnRs4PVX1NS4vs49WzMT6eb2eNp8+XuYeedDPItW/pfAf+y/rhVMsIHLlFBa\nkRzdxPTsTJM311TWgaiWiclp9Rld63FtVtAbBHzz6QKBgQDm/Mvs7DF5EfmhjP+D\ngNHaK6F+tsYE/XwYS0uDPncWbJ7CurRGQdB4XAd4odIHg7AVNmqSuwNDz3AH4dsG\nyGGQ3j3yq0rSYsUOWycVt6JSPZvyNuRDJxUiHWYbiFerpEe1kg9SMoMQXtsMsDFI\nR7VsBff1p3/efJcrMfHL1NClpwKBgQDNmDo/O6CrwtaCOUVJ//Rxzf7MWRK65+mr\naMEhX3ITiHUm1QtMuvHE+hLU4Ka+E9wsJqq4qqchXBr1v8ylHFJhIOdRSR5/MG1f\nLnTsRf51HsGNjQDsqAmqF0WLoU2ZZ0/b+MsBbaL7+GUPaNslRPJZi+agANjMZMwl\nq3OpwPbRuwKBgBAKSAL41+qnY+VjDC9Ol8QFuZ46BQA9tgtd1y2S/eQRwOiW3IPw\neBCTm3U2D4a0D1s5vybXU7+2vPnfJj2PVq8fr7+VQ4nej/6SN+GbMetyGc01IJ7F\nLQOEdR2+VxA1RUGHlgbIOS++1olIBvQU/rU0qOZnLkr97eVy/25/JcoLAoGALA6f\nDMXeXHBYP3e+XWk4HNsj6u57kQn5jP3ZxSkK7Ryk3jlxPnQhMzDTsEKj+L+QwvVW\nSFRplECEln0PgaJcFOxUJZshqefayDbQX4FwUfDRUWAR/qTTzVtHT/C1DFaTSnQ6\nLIguEQjdvzudGpN3y7CrL0Z/Lu26wafIFWyAd9kCgYBZTUrlgNmX0KEG0lwW+Gp4\nDRDrv5wwObfySKkez/g6Gm3IfUpBJuSyDZoAuTka4IKU4jybKWE16/qIpQth5u1Z\n9i4TzKDXODLgD//I1kDEl6H98fD2LPGjyIcQzAtsl9qVkjBRBZn/6KkKRkd8esZ9\n9vMIa4yP+R5BdznCBprR6A==\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-56cwd@experience-gen.iam.gserviceaccount.com",
        "client_id": "112011830418533229556",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-56cwd%40experience-gen.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com",
    })
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://experience-gen-default-rtdb.asia-southeast1.firebasedatabase.app//',
        'storageBucket': 'experience-gen.appspot.com',
        # 'databaseURL' : '데이터 베이스 url'
    })


def SaveFirebaseStorage(fileName, firstFlag):
    # if firstFlag==True:

    # Put your local file path

    # refs=firebase_admin.storage.bucket().list_blobs()
    # for index,ref in enumerate(refs):
    #     print(index,print(type(ref)),ref)
    # # print(ref)

    # with open(fileName, "wb") as f:
    #     binaryImage=f.read()
    # binaryImage=base64.b64encode(binaryImage)
    # binaryImage=binaryImage.decode("UTF-8")
    #
    #
    #
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
    blob.make_public()
    print("your file url", blob.public_url)


def format_report(request, client):
    response = client.run_report(request)

    # Row index
    row_index_names = [header.name for header in response.dimension_headers]
    row_header = []
    for i in range(len(row_index_names)):
        row_header.append([row.dimension_values[i].value for row in response.rows])

    row_index_named = pd.MultiIndex.from_arrays(np.array(row_header), names=np.array(row_index_names))
    # Row flat data
    metric_names = [header.name for header in response.metric_headers]
    data_values = []
    for i in range(len(metric_names)):
        data_values.append([row.metric_values[i].value for row in response.rows])

    output = pd.DataFrame(data=np.transpose(np.array(data_values, dtype='f')),
                          index=row_index_named, columns=metric_names)
    return output


# -----------REV230714 사이트4개 추가-----------------
def calculate_remaining_days(target_date_str):
    target_date = datetime.datetime.fromisoformat(target_date_str[:-1])
    current_date = datetime.datetime.now()
    remaining_days = (target_date - current_date).days

    return remaining_days


def GetReviewPlace():
    dataList = []
    categorys = ['제품', '지역']
    for category in categorys:
        count = 0
        while True:
            cookies = {
                'PHPSESSID': 'clgj4atiom9e19agkj8nj51pdi',
                '_gcl_au': '1.1.25152803.1689058359',
                '_fbp': 'fb.2.1689058359432.428743364',
                '_gid': 'GA1.3.533737594.1689058360',
                'e1192aefb64683cc97abb83c71057733': 'cHJvZHVjdA%3D%3D',
                '_gat_UA-213777995-1': '1',
                'wcs_bt': 's_502a9426297b:1689058717',
                '_ga_4XZ5KL34H1': 'GS1.1.1689058359.1.1.1689058717.0.0.0',
                '_ga': 'GA1.1.123397818.1689058360',
            }

            headers = {
                'authority': 'www.reviewplace.co.kr',
                'accept': 'text/html, */*; q=0.01',
                'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
                # 'cookie': 'PHPSESSID=clgj4atiom9e19agkj8nj51pdi; _gcl_au=1.1.25152803.1689058359; _fbp=fb.2.1689058359432.428743364; _gid=GA1.3.533737594.1689058360; e1192aefb64683cc97abb83c71057733=cHJvZHVjdA%3D%3D; _gat_UA-213777995-1=1; wcs_bt=s_502a9426297b:1689058717; _ga_4XZ5KL34H1=GS1.1.1689058359.1.1.1689058717.0.0.0; _ga=GA1.1.123397818.1689058360',
                'if-modified-since': 'Tue, 11 Jul 2023 06:58:23 GMT',
                'referer': 'https://www.reviewplace.co.kr/pr/?ct1=%EC%A0%9C%ED%92%88',
                'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                'x-requested-with': 'XMLHttpRequest',
            }

            params = {
                'ct1': str(category),
                'device': 'pc',
                'rpage': str(count),
            }

            response = requests.get(
                'https://www.reviewplace.co.kr/theme/rp/_ajax_cmp_list_tpl.php',
                params=params,
                cookies=cookies,
                headers=headers,
            )

            soup = BeautifulSoup(response.text, 'lxml')
            # print(soup.prettify())

            items = soup.find_all('div', attrs={'class': 'item'})
            print("갯수는:", len(items))
            if len(items) == 0:
                break
            for item in items:
                title = item.find('p', attrs={'class': 'tit'}).get_text()
                if category=="제품":
                    title=title+"(배송형)"
                region = ""
                try:
                    dday = item.find('p', attrs={'class': 'date'}).get_text()
                    regex = re.compile("\d+")
                    dday = regex.findall(dday)[0]
                except:
                    dday = '0'
                applyDemandCount = item.find('div', attrs={'class': 'num'}).get_text()
                applyCount = regex.findall(applyDemandCount)[0]
                demandCount = regex.findall(applyDemandCount)[1]
                imageUrl = item.find('img')['src']
                url = 'https://www.reviewplace.co.kr' + item.find('a')['href']
                myIndex = regex.findall(url)[-1]

                data = {'platform': '리뷰플레이스', 'region': region, 'dday': dday, 'title': title, 'applyCount': applyCount,
                        'demandCount': demandCount, 'imageUrl': imageUrl, 'url': url, 'myImage': "리뷰플레이스_" + myIndex}
                print(data)
                dataList.append(data)
            print(category, "/", "갯수는:", len(dataList))
            count += 1
            time.sleep(random.randint(5, 10) * 0.1)
    return dataList


def GetChvu():
    dataList = []
    cookies = {
        'wcs_bt': '7477ac737b2058:1689062251',
        '_ga': 'GA1.1.883970942.1689062252',
        '_ga_7EX0VJYMCT': 'GS1.1.1689062251.1.1.1689062298.0.0.0',
    }

    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        # 'Cookie': 'wcs_bt=7477ac737b2058:1689062251; _ga=GA1.1.883970942.1689062252; _ga_7EX0VJYMCT=GS1.1.1689062251.1.1.1689062298.0.0.0',
        'Referer': 'https://chvu.co.kr/campaign',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    response = requests.get(
        'https://chvu.co.kr/api/campaign/getCampaignByCondition?limitNumber=2000&startIndex=0&conditions=%7B%22channel%22:%7B%22all%22:true,%22insta%22:false,%22blog%22:false,%22youtube%22:false,%22misc%22:false%7D,%22activity%22:%7B%22all%22:false,%22visit%22:true,%22delivery%22:true,%22report%22:false,%22misc%22:false,%22purchase%22:false%7D,%22locations%22:[],%22service%22:%7B%22all%22:true,%22travel%22:false,%22hotplaces%22:false,%22beauty%22:false,%22fashion%22:false,%22food%22:false,%22life%22:false,%22parenting%22:false,%22misc%22:false%7D,%22point%22:%7B%22all%22:true,%22firstBracket%22:false,%22secondBracket%22:false,%22thirdBracket%22:false,%22fourthBracket%22:false,%22fifthBracket%22:false%7D%7D&searchString=&sortCondition=deadline',
        cookies=cookies,
        headers=headers,
    )
    results = json.loads(response.text)
    # pprint.pprint(results)
    for index, result in enumerate(results):
        # print(result)
        title = result['title']
        try:
            isBaesong=result['activity']
        except:
            isBaesong=""
        if isBaesong=="delivery":
            title=title+"(배송형)"



        region = ""
        dday = str(calculate_remaining_days(result['appl_end_date']) + 2)
        applyCount = result['current_applicants']
        demandCount = result['reviewer_limit']
        imageUrl = "https://chvu.co.kr/" + result['main_img']
        url = 'https://chvu.co.kr/campaign/' + str(result['campaign_id'])
        myIndex = str(result['campaign_id'])

        if float(dday) < 0:
            break

        data = {'platform': '체험뷰', 'region': region, 'dday': dday, 'title': title, 'applyCount': applyCount,
                'demandCount': demandCount, 'imageUrl': imageUrl, 'url': url, 'myImage': "체험뷰_" + myIndex}
        print(data)
        dataList.append(data)
    print("데이타갯수:", len(dataList))
    return dataList


def GetReviewNote():

    dataList = []
    endFlag = False

    cookies = {
        '_ga': 'GA1.1.1345229672.1701352846',
        'token': '',
        '_ga_XZVSWF43K1': 'GS1.1.1701352845.1.1.1701353347.0.0.0',
    }

    headers = {
        'authority': 'www.reviewnote.co.kr',
        'accept': '*/*',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        # 'cookie': '_ga=GA1.1.1345229672.1701352846; token=; _ga_XZVSWF43K1=GS1.1.1701352845.1.1.1701353347.0.0.0',
        'if-none-match': 'W/"icdfkhbu42t6v"',
        'purpose': 'prefetch',
        'referer': 'https://www.reviewnote.co.kr/',
        'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        'x-nextjs-data': '1',
    }

    response = requests.get(
        'https://www.reviewnote.co.kr/_next/data/WMgmkUgb2Bg03IhoR8n-6/ko/campaigns.json',
        cookies=cookies,
        headers=headers,
    )
    decoded_content = response.content.decode('utf-8')
    results = json.loads(decoded_content)['pageProps']['data']
    # pprint.pprint(results)

    for result in results:
        # pprint.pprint(result)
        title = result['title']
        isBaesong=result['sort']
        if isBaesong==True:
            title=title+"(배송형)"
        region = ""
        dday = calculate_remaining_days(result['applyEndAt'])
        if dday <= 0:
            dday = 9999
        applyCount = result['applicantCount']
        demandCount = result['infNum']
        imageKey = result['imageKey']
        if imageKey == None:
            imageUrl = ""
        else:
            imageUrl = 'https://www.reviewnote.co.kr/_next/image?url=https%3A%2F%2Ffirebasestorage.googleapis.com%2Fv0%2Fb%2Freviewnote-e92d9.appspot.com%2Fo%2Fitems%252F{}%3Falt%3Dmedia&w=1080&q=75'.format(
                result['imageKey'].replace("items/", ""))

        url = 'https://www.reviewnote.co.kr/campaigns/{}'.format(str(result['id']))
        myIndex = str(result['id'])
        data = {'platform': '리뷰노트', 'region': region, 'dday': dday, 'title': title, 'applyCount': applyCount,
                'demandCount': demandCount, 'imageUrl': imageUrl, 'url': url, 'myImage': "리뷰노트_" + myIndex}
        print(data)
        dataList.append(data)
    print("갯수는:", len(dataList))


def GetCloudView():
    dataList = []
    categorys = ['https://www.cloudreview.co.kr/campaign/delivery', 'https://www.cloudreview.co.kr/campaign/exp',
                 'https://www.cloudreview.co.kr/campaign/review', 'https://www.cloudreview.co.kr/campaign/shopping']
    for category in categorys:
        cookies = {
            'sessions': 'e65857a0c695575b1585a1c4eea80eb4c0151d2e',
            '_gid': 'GA1.3.1393034719.1689074042',
            '_gat_gtag_UA_130885233_1': '1',
            '_ga_Y4WT55P82W': 'GS1.1.1689074041.1.1.1689074168.0.0.0',
            '_ga_175K0Y868Z': 'GS1.1.1689074042.1.1.1689074169.0.0.0',
            '_ga': 'GA1.3.2096767969.1689074041',
        }

        headers = {
            'authority': 'www.cloudreview.co.kr',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            # 'cookie': 'sessions=e65857a0c695575b1585a1c4eea80eb4c0151d2e; _gid=GA1.3.1393034719.1689074042; _gat_gtag_UA_130885233_1=1; _ga_Y4WT55P82W=GS1.1.1689074041.1.1.1689074168.0.0.0; _ga_175K0Y868Z=GS1.1.1689074042.1.1.1689074169.0.0.0; _ga=GA1.3.2096767969.1689074041',
            'referer': 'https://www.cloudreview.co.kr/campaign/delivery',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'document',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-user': '?1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }

        response = requests.get(category, cookies=cookies, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        itemAll = soup.find_all('div', attrs={'class': 'col-xl-1 col-lg-3 col-md-4 col-sm-6 col-6'})

        for item in itemAll:

            title = item.find('div', attrs={'class': 'card-title'}).get_text().strip()
            if category.find('delivery')>=0:
                title=title+"(배송형)"
            region = ""
            dday = item.find('span', attrs={'class': 'card-text-right'}).get_text().strip()
            regex = re.compile("\d+")
            try:
                dday = regex.findall(dday)[0]
            except:
                dday = "0"
            applyDemandCount = item.find('small', attrs={'class': 'text-muted people-count-text'}).get_text()
            applyCount = regex.findall(applyDemandCount)[0]
            demandCount = regex.findall(applyDemandCount)[1]
            imageUrl = 'https://www.cloudreview.co.kr' + item.find('a').find('img')['data-original']

            url = 'https://www.cloudreview.co.kr' + item.find('a')['href']
            myIndex = item.find('a')['href'].split("/")[-1]

            # -----------배송형 확인
            btns = item.find_all('button', attrs={'class': 'btn btn-sm btn-outline-secondary'})
            reviewTypes = ""

            for btn in btns:
                reviewType = "(" + btn.get_text().strip() + ")"
                if reviewType.find("배송") >= 0:
                    reviewTypes = reviewTypes + reviewType
            if len(reviewTypes) >= 1:
                title = title + reviewTypes

            data = {'platform': '클라우드리뷰', 'region': region, 'dday': dday, 'title': title, 'applyCount': applyCount,
                    'demandCount': demandCount, 'imageUrl': imageUrl, 'url': url, 'myImage': "클라우드리뷰_" + myIndex}
            print(data)
            dataList.append(data)
        print("========================================")
        print("상품수:", len(dataList))
    return dataList

def GetTble():
    dataList=[]
    categorys=['l','p']
    for category in categorys:
        cookies = {
            'PHPSESSID': '427rlk1g9hmljdqp9cjb0mnui7',
            '421f3aa67b14f0aef550c43224e4769c': 'MjAyMzA5MTExMTI5MjYyMA%3D%3D',
            '_gid': 'GA1.2.2000416362.1694399391',
            '_fbp': 'fb.1.1694399391295.673335596',
            '_ga_45WS59V01V': 'GS1.1.1694399390.1.1.1694400699.0.0.0',
            '_ga': 'GA1.1.946830042.1694399391',
        }

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Connection': 'keep-alive',
            # 'Cookie': 'PHPSESSID=427rlk1g9hmljdqp9cjb0mnui7; 421f3aa67b14f0aef550c43224e4769c=MjAyMzA5MTExMTI5MjYyMA%3D%3D; _gid=GA1.2.2000416362.1694399391; _fbp=fb.1.1694399391295.673335596; _ga_45WS59V01V=GS1.1.1694399390.1.1.1694400699.0.0.0; _ga=GA1.1.946830042.1694399391',
            'If-Modified-Since': 'Mon, 11 Sep 2023 02:46:57 GMT',
            'Referer': 'https://www.tble.kr/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        params = {
            'type': category,
            'blog': '블로그',
            'blog2': '인스타',
        }

        requests.packages.urllib3.disable_warnings()
        requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
        try:
            requests.packages.urllib3.contrib.pyopenssl.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
        except AttributeError:
            # no pyopenssl support used / needed / available
            pass

        response = requests.get('https://www.tble.kr/category.php', params=params, cookies=cookies, headers=headers,verify=False)
        soup=BeautifulSoup(response.text,'lxml')
        # print(soup.prettify())

        itemGroup=soup.find('div',attrs={'sub_container review'})
        items=itemGroup.find_all('div',attrs={'class':'item'})
        for item in items:
            try:
                title=item.find("div",attrs={'class':'t2'}).get_text()
                if category=="p":
                    title=title+"(배송형)"
            except:
                title=""
            print('title:',title)
            try:
                applyCount=item.find("div",attrs={'class':'t4'}).find_all('strong')[0].get_text()
            except:
                applyCount=""
            print('applyCount:',applyCount)

            try:
                demandCount=item.find("div",attrs={'class':'t4'}).find_all('strong')[1].get_text()
            except:
                demandCount=""
            print('demandCount:',demandCount)
            region=""
            try:
                imageUrl=item.find("div",attrs={'class':'img'}).find('img')['src']
            except:
                imageUrl=""
            print('imageUrl:',imageUrl)

            try:
                url='https://www.tble.kr/'+item.find("div",attrs={'class':'img'}).find('a')['href']
            except:
                url=""
            print('url:',url)

            try:
                regex=re.compile("\d+")
                myIndex=regex.findall(url)[0]
            except:
                myIndex=""
            print('myIndex:',myIndex)

            try:
                dday = item.find("div", attrs={'class': 't1'}).find_all('span')[-1].get_text()
                if dday.find("오늘 마감")>=0:
                    dday=0
                else:
                    regex=re.compile("\d+")
                    dday=regex.findall(dday)[0]
            except:
                dday=""
            print('dday:',dday)

            data = {'platform': '티블', 'region': region, 'dday': dday, 'title': title, 'applyCount': applyCount,
                    'demandCount': demandCount, 'imageUrl': imageUrl, 'url': url, 'myImage': "티블_" + myIndex}
            # print(data)
            dataList.append(data)
    print("총갯수:", len(dataList))
    return dataList

# =============REV AWS S3 그림 업로드

def UploadImageToS3(file_path):
    # AWS 계정의 액세스 키와 시크릿 키를 설정합니다.
    aws_access_key_id = 'AKIAYULRLDL2STEXU6SD'
    aws_secret_access_key = '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'

    bucket_name="exgen"

    # S3 클라이언트를 생성합니다.
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    # print(s3_client)
    # 그림 파일을 S3 버킷에 업로드합니다.
    try:
        s3_client.upload_file(file_path, bucket_name, file_path)
        print("파일 업로드 성공!")
    except Exception as e:
        print("파일 업로드 실패:", e)

# def GetFileList():
#     # AWS 계정의 액세스 키와 시크릿 키를 설정합니다.
#     aws_access_key_id = 'AKIAYULRLDL2STEXU6SD'
#     aws_secret_access_key = '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'
#     bucket_name="exgen"
#
#     s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
#
#     objLists=s3_client.list_objects(Bucket=bucket_name)['Contents']
#     filenameList=[]
#     for objList in objLists:
#         filename=objList['Key']
#         filenameList.append(filename)
#     print(filenameList)
#     return filenameList
def GetFileList():
    """Get a list of all keys in an S3 bucket."""
    aws_access_key_id = 'AKIAYULRLDL2STEXU6SD'
    aws_secret_access_key = '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'

    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    bucket='exgen'
    # s3 = boto3.client('s3')
    keys = []

    kwargs = {'Bucket': bucket}
    while True:
        resp = s3.list_objects_v2(**kwargs)
        for obj in resp['Contents']:
            keys.append(obj['Key'])

        try:
            kwargs['ContinuationToken'] = resp['NextContinuationToken']
        except KeyError:
            break
    print("전체그림수:",len(keys))
    return keys

#===================================


def GetProducts(keyword):
    url = 'https://f36dcjopejicrmfh3tq2bavmbe0ljydb.lambda-url.ap-northeast-2.on.aws/getProducts'
    data = json.dumps(keyword)
    res = requests.get(url, params=keyword)
    print(res.text)
    result = json.loads(res.text)
    pprint.pprint(result)
    return result


def AddProducts(totalList):
    print(totalList)
    url = 'https://f36dcjopejicrmfh3tq2bavmbe0ljydb.lambda-url.ap-northeast-2.on.aws/addProducts'
    data = totalList
    res = requests.post(url, data=json.dumps(data))
    print("status_code:",res.status_code)
    result = json.loads(res.text)
    print(res.text)


def GetRemove():
    url = 'https://f36dcjopejicrmfh3tq2bavmbe0ljydb.lambda-url.ap-northeast-2.on.aws/removeProducts'
    res = requests.delete(url)
    print(res.text)


def DeleteAllImage():
    """Get a list of all keys in an S3 bucket."""
    aws_access_key_id = 'AKIAYULRLDL2STEXU6SD'
    aws_secret_access_key = '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'

    # s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    s3 = boto3.resource('s3')
    buckets = s3.Bucket(name="exgen")

    keys = GetFileList()
    print('갯수는', len(keys))
    with open('keys.json', 'w', encoding='utf-8-sig') as f:
        json.dump(keys, f, indent=2, ensure_ascii=False)
    for index, key in enumerate(keys):
        print(index, "번째 삭제중..")
        resp = s3.Object('exgen', key).delete()

# ------------------------------------------------
# class Thread(QThread):
#     cnt = 0
#     user_signal = pyqtSignal(str)  # 사용자 정의 시그널 2 생성
#
#     def __init__(self, parent, timeCycle):  # parent는 WndowClass에서 전달하는 self이다.(WidnowClass의 인스턴스)
#         super().__init__(parent)
#         self.parent = parent  # self.parent를 사용하여 WindowClass 위젯을 제어할 수 있다.
#         self.timeCycle = timeCycle
#
#     def run(self):
#         timePrev = 0
#         InitFirebase()
#         print("주기는:", self.timeCycle)
#         while True:
#
#             timeNow = datetime.datetime.now().timestamp()
#             timeNowString = datetime.datetime.now().strftime("%H%M")
#             try:
#                 print("현재타임:",timeNowString,"예약타임:",self.timeCycle)
#                 if timeNowString == self.timeCycle:
#                 # if True:
#                     # ---------------GA4 결과 가져오기
#                     print("ga4 조회중")
#                     os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'credential.json'
#                     property_id = '378226211'
#                     client = BetaAnalyticsDataClient()
#                     start_date = datetime.datetime.now() - datetime.timedelta(days=5)
#                     start_date_string = start_date.strftime("%Y-%m-%d")
#                     request = RunReportRequest(
#                         property='properties/' + property_id,
#                         dimensions=[Dimension(name="day")],
#                         metrics=[Metric(name="activeUsers")],
#                         order_bys=[OrderBy(dimension={'dimension_name': 'day'})],
#                         date_ranges=[DateRange(start_date=start_date_string, end_date="today")],
#                     )
#                     # print(request)
#                     print("request완료")
#                     output_df = format_report(request, client)
#                     print(output_df)
#                     visitorsList = output_df['activeUsers'].tolist()
#                     newData = []
#                     if len(visitorsList) == 6:
#                         dateConstant = 5
#                     else:
#                         dateConstant = 4
#                     for index, visitorsElem in enumerate(visitorsList):
#                         targetTime = datetime.datetime.now() - datetime.timedelta(days=(dateConstant - index))
#                         targetTimeString = targetTime.strftime("%m/%d")
#                         data = {'name': targetTimeString, 'visitors': visitorsElem}
#                         newData.append(data)
#                     print(newData)
#                     SaveFirebaseVisitors(newData)
#
#                     # --------------REV230719 토큰저장---------------
#
#                     # regiToken = 'ZJ1kCQALAAET_cVonhTo2P2DT5W4'
#                     # SaveFirebaseRegiToken(regiToken)
#                     # print("토큰저장완료")
#
#                     # -----------------------------------------
#
#                     timePrev = datetime.datetime.now().timestamp()
#                     text = "크롤링 시작 / {}".format(timeNowString)
#                     self.user_signal.emit(text)
#
#                     try:
#                         dataList1 = GetGangNam()  # 강남맛집 검색
#                         text = "강남맛집 크롤링 완료"
#                     except:
#                         dataList1 = []
#                         text = "강남맛집 크롤링 실패"
#
#                     print(text)
#                     self.user_signal.emit(text)
#
#                     try:
#                         dataList2 = GetNolowa()  # 놀러와 검색
#                         text = "놀러와체험단 크롤링 완료"
#                     except:
#                         dataList2 = []
#                         text = "놀러와체험단 크롤링 실패"
#
#                     print(text)
#                     self.user_signal.emit(text)
#
#                     try:
#                         dataList3 = GetDinnerQueen()  # 디너의여왕 검색
#                         text = "디너의여왕 크롤링 완료"
#                     except:
#                         dataList3 = []
#                         text = "디너의여왕 크롤링 실패"
#
#                     print(text)
#                     self.user_signal.emit(text)
#
#                     try:
#                         dataList4 = GetDailyView()  # 데일리뷰 검색
#                         text = "데일리뷰 크롤링 완료"
#                     except:
#                         dataList4 = []
#                         text = "데일리뷰 크롤링 실패"
#                     print(text)
#                     self.user_signal.emit(text)
#
#                     # ===============6월21일 사이트5개 추가Start
#
#                     try:
#                         dataList5 = GetGaBoJa()
#                         text = "가보자체험단 크롤링 완료"
#                     except:
#                         dataList5 = []
#                         text = "가보자체험단 크롤링 실패"
#                     print(text)
#                     self.user_signal.emit(text)
#
#                     try:
#                         dataList6 = GetMrBlog()
#                         text = "미스터블로그 크롤링 완료"
#                     except:
#                         dataList6 = []
#                         text = "미스터블로그 크롤링 실패"
#                     print(text)
#                     self.user_signal.emit(text)
#
#                     try:
#                         dataList7 = GetOhMyBlog()
#                         text = "오마이블로그 크롤링 완료"
#                     except:
#                         dataList7 = []
#                         text = "오마이블로그 크롤링 실패"
#                     print(text)
#                     self.user_signal.emit(text)
#
#                     try:
#                         dataList8 = GetSeoulObba()
#                         text = "서울오빠 크롤링 완료"
#                     except:
#                         dataList8 = []
#                         text = "서울오빠 크롤링 실패"
#                     print(text)
#                     self.user_signal.emit(text)
#
#                     try:
#                         dataList9 = GetRevu()
#                         text = "레뷰 크롤링 완료"
#                     except:
#                         dataList9 = []
#                         text = "레뷰 크롤링 실패"
#                     print(text)
#                     self.user_signal.emit(text)
#
#                     # ===============6월21일 사이트5개 추가End
#
#                     # ==============7월14일 4개 추가
#
#                     try:
#                         dataList10 = GetReviewPlace()
#                         text = "리뷰플레이스 크롤링 완료"
#                     except:
#                         dataList10 = []
#                         text = "리뷰플레이스 크롤링 실패"
#                     print(text)
#                     self.user_signal.emit(text)
#                     try:
#                         dataList11 = GetChvu()
#                         text = "체험뷰 크롤링 완료"
#                     except:
#                         dataList11 = []
#                         text = "체험뷰 크롤링 실패"
#                     print(text)
#                     self.user_signal.emit(text)
#
#                     try:
#                         dataList12 = GetReviewNote()
#                         text = "리뷰노트 크롤링 완료"
#                     except:
#                         dataList12 = []
#                         text = "리뷰노트 크롤링 실패"
#                     print(text)
#                     self.user_signal.emit(text)
#                     try:
#                         dataList13 = GetCloudView()
#                         text = "클라우드뷰 크롤링 완료"
#                     except:
#                         dataList13 = []
#                         text = "클라우드뷰 크롤링 실패"
#                     print(text)
#                     self.user_signal.emit(text)
#
#                     try:
#                         dataList14 = GetTble()
#                         text = "티블 크롤링 완료"
#                     except:
#                         dataList14 = []
#                         text = "티블 크롤링 실패"
#                     print(text)
#                     self.user_signal.emit(text)
#
#                     totalList = dataList1 + dataList2 + dataList3 + dataList4 + dataList5 + dataList6 + dataList7 + dataList8 + dataList9 + dataList10 + dataList11 + dataList12 + dataList13 + dataList14  # 검색결과를 모두 합친다.
#
#                     with open('totalList.json', 'w',encoding='utf-8-sig') as f:
#                         json.dump(totalList, f, indent=2,ensure_ascii=False)
#
#
#
#                     with open('totalList.json', 'w') as f:
#                         json.dump(totalList, f, indent=2)
#
#                     text = "전체 글 갯수:{}".format(len(totalList))
#                     print(text)
#                     self.user_signal.emit(text)
#
#                     print("지우기 시작")
#                     GetRemove()  # 변동부
#                     print("지우기 완료")
#
#                     text="지우기완료"
#                     self.user_signal.emit(text)
#
#                     print("데이타저장하기")
#                     for i in range(0, len(totalList), 200):
#                         while True:
#                             try:
#                                 splitList=totalList[i:i + 200]
#                                 AddProducts(splitList)
#                                 break
#                             except:
#                                 print("에러발생")
#                         time.sleep(0.2)
#                         print("전송완료")
#                     text = "데이타 저장 완료"
#                     print(text)
#                     self.user_signal.emit(text)
#
#                     # ====================그림파일 저장부============
#                     text = "그림 다운로드 중..."
#                     print(text)
#                     self.user_signal.emit(text)
#                     print("그림파일 가져오기")
#                     firstFlag = True
#                     for index, totalElem in enumerate(totalList):
#
#                         filename = "{}.png".format(totalElem['myImage'])
#                         # print("{}번째 파일".format(index), filename)
#
#                         if firstFlag == True:
#                             # InitFirebaseStorage() #테스트에서만 켬
#                             bucketList = GetFileList()
#
#                             # pprint.pprint(bucketList)
#                             preGetList = []
#                             for bucketElem in bucketList:
#                                 # print('filename:',filename)
#                                 # print(str(bucketElem))
#                                 data = str(bucketElem)
#                                 preGetList.append(data)
#                             # print('preGetList:', preGetList)
#                             # print("그림갯수:", len(preGetList))
#                             firstFlag = False
#                         # print('filename:', filename)
#                         skip_flag = False
#                         for preGetElem in preGetList:
#                             if preGetElem.find(filename) >= 0:
#                                 print("그림이미있음".format(filename))
#                                 skip_flag = True
#                                 break
#                         if skip_flag == True:
#                             continue
#
#                         try:
#                             headers = {
#                                 "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"}
#                             imageUrl = totalElem['imageUrl']
#                             if imageUrl.find("no_img") >= 0 or len(imageUrl) == 0:
#                                 continue
#                             print('{}번째 imageUrl:'.format(index), imageUrl)
#                             image_res = requests.get(imageUrl, headers=headers,timeout=10)  # 그림파일 저장
#                             image_res.raise_for_status()
#
#                             with open(filename, "wb") as f:
#                                 f.write(image_res.content)  # 그림파일 각각 저장
#                             text = "그림파일 저장중..."
#                             print(text)
#                             # SaveFirebaseStorage(filename, firstFlag)
#                             UploadImageToS3(filename)
#                             print('그림삭제')
#                             # 파일이 존재하는지 확인 후 삭제
#                             if os.path.exists(filename):
#                                 os.remove(filename)
#                                 print(f"File {filename} has been deleted.")
#                             else:
#                                 print(f"File {filename} does not exist.")
#                             time.sleep(random.randint(5, 10) * 0.1)
#
#                         except:
#                             print("에러로건너뜀")
#                             time.sleep(1)
#
#                         print("=====================================")
#                     text = "그림 다운로드 완료"
#                     print(text)
#                     self.user_signal.emit(text)
#                 # ===================================================================
#                 else:
#                     text = "대기중..."
#                     self.user_signal.emit(text)
#
#
#             except:
#                 print("에러로 한텀쉬기")
#                 time.sleep(60 * 10)
#             time.sleep(10)
#
#     def stop(self):
#         pass
#
#
# class Example(QMainWindow, Ui_MainWindow):
#     def __init__(self):
#         super().__init__()
#         self.path = "C:"
#         self.index = None
#         self.setupUi(self)
#         self.setSlot()
#         self.show()
#         QApplication.processEvents()
#         self.timeEdit.setTime(QTime(3,0))
#
#     def start(self):
#         print('11')
#         self.timeCycle=str(self.timeEdit.time().hour())+"_"+str(self.timeEdit.time().minute())
#
#         self.timeCycle=datetime.datetime.strptime(self.timeCycle,"%H_%M").strftime("%H%M")
#         print('self.timeCycle:',self.timeCycle)
#         self.x = Thread(self, self.timeCycle)
#         self.x.user_signal.connect(self.slot1)  # 사용자 정의 시그널2 슬롯 Connect
#         self.x.start()
#
#     def slot1(self, data1):  # 사용자 정의 시그널1에 connect된 function
#         self.textEdit.append(str(data1))
#
#     def setSlot(self):
#         pass
#
#     def setIndex(self, index):
#         pass
#
#     def quit(self):
#         QCoreApplication.instance().quit()
#
#
# app = QApplication([])
# ex = Example()
# sys.exit(app.exec_())

timeCycle="0100"
timePrev = 0
InitFirebase()
print("주기는:", timeCycle)
firstFlag=True
while True:
    timeNow = datetime.datetime.now().timestamp()
    timeNowString = datetime.datetime.now().strftime("%H%M")
    try:
        print("현재타임:",timeNowString,"예약타임:",timeCycle)
        if timeNowString == timeCycle or firstFlag==True:
            firstFlag=False
            # ---------------GA4 결과 가져오기
            print("ga4 조회중")
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'credential.json'
            property_id = '378226211'
            client = BetaAnalyticsDataClient()
            start_date = datetime.datetime.now() - datetime.timedelta(days=5)
            start_date_string = start_date.strftime("%Y-%m-%d")
            request = RunReportRequest(
                property='properties/' + property_id,
                dimensions=[Dimension(name="day")],
                metrics=[Metric(name="activeUsers")],
                order_bys=[OrderBy(dimension={'dimension_name': 'day'})],
                date_ranges=[DateRange(start_date=start_date_string, end_date="today")],
            )
            # print(request)
            print("request완료")
            output_df = format_report(request, client)
            print(output_df)
            visitorsList = output_df['activeUsers'].tolist()
            newData = []
            if len(visitorsList) == 6:
                dateConstant = 5
            else:
                dateConstant = 4
            for index, visitorsElem in enumerate(visitorsList):
                targetTime = datetime.datetime.now() - datetime.timedelta(days=(dateConstant - index))
                targetTimeString = targetTime.strftime("%m/%d")
                data = {'name': targetTimeString, 'visitors': visitorsElem}
                newData.append(data)
            print(newData)
            SaveFirebaseVisitors(newData)

            # --------------REV230719 토큰저장---------------

            # regiToken = 'ZJ1kCQALAAET_cVonhTo2P2DT5W4'
            # SaveFirebaseRegiToken(regiToken)
            # print("토큰저장완료")

            # -----------------------------------------

            timePrev = datetime.datetime.now().timestamp()
            text = "크롤링 시작 / {}".format(timeNowString)

            try:
                dataList1 = GetGangNam()  # 강남맛집 검색
                text = "강남맛집 크롤링 완료"
            except:
                dataList1 = []
                text = "강남맛집 크롤링 실패"

            print(text)

            try:
                dataList2 = GetNolowa()  # 놀러와 검색
                text = "놀러와체험단 크롤링 완료"
            except:
                dataList2 = []
                text = "놀러와체험단 크롤링 실패"

            print(text)

            try:
                dataList3 = GetDinnerQueen()  # 디너의여왕 검색
                text = "디너의여왕 크롤링 완료"
            except:
                dataList3 = []
                text = "디너의여왕 크롤링 실패"

            print(text)

            try:
                dataList4 = GetDailyView()  # 데일리뷰 검색
                text = "데일리뷰 크롤링 완료"
            except:
                dataList4 = []
                text = "데일리뷰 크롤링 실패"
            print(text)

            # ===============6월21일 사이트5개 추가Start

            try:
                dataList5 = GetGaBoJa()
                text = "가보자체험단 크롤링 완료"
            except:
                dataList5 = []
                text = "가보자체험단 크롤링 실패"
            print(text)

            try:
                dataList6 = GetMrBlog()
                text = "미스터블로그 크롤링 완료"
            except:
                dataList6 = []
                text = "미스터블로그 크롤링 실패"
            print(text)

            try:
                dataList7 = GetOhMyBlog()
                text = "오마이블로그 크롤링 완료"
            except:
                dataList7 = []
                text = "오마이블로그 크롤링 실패"
            print(text)

            try:
                dataList8 = GetSeoulObba()
                text = "서울오빠 크롤링 완료"
            except:
                dataList8 = []
                text = "서울오빠 크롤링 실패"
            print(text)

            try:
                dataList9 = GetRevu()
                text = "레뷰 크롤링 완료"
            except:
                dataList9 = []
                text = "레뷰 크롤링 실패"
            print(text)

            # ===============6월21일 사이트5개 추가End

            # ==============7월14일 4개 추가

            try:
                dataList10 = GetReviewPlace()
                text = "리뷰플레이스 크롤링 완료"
            except:
                dataList10 = []
                text = "리뷰플레이스 크롤링 실패"
            print(text)
            try:
                dataList11 = GetChvu()
                text = "체험뷰 크롤링 완료"
            except:
                dataList11 = []
                text = "체험뷰 크롤링 실패"
            print(text)

            try:
                dataList12 = GetReviewNote()
                text = "리뷰노트 크롤링 완료"
            except:
                dataList12 = []
                text = "리뷰노트 크롤링 실패"
            print(text)
            try:
                dataList13 = GetCloudView()
                text = "클라우드뷰 크롤링 완료"
            except:
                dataList13 = []
                text = "클라우드뷰 크롤링 실패"
            print(text)

            try:
                dataList14 = GetTble()
                text = "티블 크롤링 완료"
            except:
                dataList14 = []
                text = "티블 크롤링 실패"
            print(text)

            totalList = dataList1 + dataList2 + dataList3 + dataList4 + dataList5 + dataList6 + dataList7 + dataList8 + dataList9 + dataList10 + dataList11 + dataList12 + dataList13 + dataList14  # 검색결과를 모두 합친다.

            with open('totalList.json', 'w',encoding='utf-8-sig') as f:
                json.dump(totalList, f, indent=2,ensure_ascii=False)

            with open('totalList.json', 'w') as f:
                json.dump(totalList, f, indent=2)

            text = "전체 글 갯수:{}".format(len(totalList))
            print(text)

            print("지우기 시작")
            GetRemove()  # 변동부
            print("지우기 완료")

            text="지우기완료"

            print("데이타저장하기")
            for i in range(0, len(totalList), 200):
                while True:
                    try:
                        splitList=totalList[i:i + 200]
                        AddProducts(splitList)
                        break
                    except:
                        print("에러발생")
                time.sleep(0.2)
                print("전송완료")
            text = "데이타 저장 완료"
            print(text)

            # ====================그림파일 저장부============
            text = "그림 다운로드 중..."
            print(text)
            print("그림파일 가져오기")
            firstFlag = True
            for index, totalElem in enumerate(totalList):

                filename = "{}.png".format(totalElem['myImage'])
                # print("{}번째 파일".format(index), filename)

                if firstFlag == True:
                    # InitFirebaseStorage() #테스트에서만 켬
                    bucketList = GetFileList()

                    # pprint.pprint(bucketList)
                    preGetList = []
                    for bucketElem in bucketList:
                        # print('filename:',filename)
                        # print(str(bucketElem))
                        data = str(bucketElem)
                        preGetList.append(data)
                    # print('preGetList:', preGetList)
                    # print("그림갯수:", len(preGetList))
                    firstFlag = False
                # print('filename:', filename)
                skip_flag = False
                for preGetElem in preGetList:
                    if preGetElem.find(filename) >= 0:
                        print("그림이미있음".format(filename))
                        skip_flag = True
                        break
                if skip_flag == True:
                    continue

                try:
                    headers = {
                        "User-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"}
                    imageUrl = totalElem['imageUrl']
                    if imageUrl.find("no_img") >= 0 or len(imageUrl) == 0:
                        continue
                    print('{}번째 imageUrl:'.format(index), imageUrl)
                    image_res = requests.get(imageUrl, headers=headers,timeout=10)  # 그림파일 저장
                    image_res.raise_for_status()

                    with open(filename, "wb") as f:
                        f.write(image_res.content)  # 그림파일 각각 저장
                    text = "그림파일 저장중..."
                    print(text)
                    # SaveFirebaseStorage(filename, firstFlag)
                    UploadImageToS3(filename)
                    print('그림삭제')
                    # 파일이 존재하는지 확인 후 삭제
                    if os.path.exists(filename):
                        os.remove(filename)
                        print(f"File {filename} has been deleted.")
                    else:
                        print(f"File {filename} does not exist.")
                    time.sleep(random.randint(5, 10) * 0.1)

                except:
                    print("에러로건너뜀")
                    time.sleep(1)

                print("=====================================")
            text = "그림 다운로드 완료"
            print(text)
        # ===================================================================
        else:
            text = "대기중..."
            print(text)


    except:
        print("에러로 한텀쉬기")
        time.sleep(60 * 10)
    time.sleep(10)






