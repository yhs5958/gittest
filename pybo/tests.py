from django.test import TestCase

# Create your tests here.
import unittest
import datetime
import logging
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

from selenium import webdriver
import time
from selenium.webdriver.common.by import By




class Crawling(unittest.TestCase):
    def setUp(self):
       #webdriver  Firefox 객체 생성
       self.brower = webdriver.Firefox(executable_path='C:\BIG_AI0102\01_PYTHON\app\geckodriver.exe')
       print('setUp')

    def tearDown(self):
        logging.info('tearDown')
        #self.brower.quit()  #webdriver 종료

    @unittest.skip('test_sel')
    def test_sel(self):
        self.brower.get('http://127.0.0.1:8000/pybo/2/')
        print('brower.title:{}'.format(self.brower.title))
        self.assertIn('Pybo', self.brower.title)

        textarea=self.brower.find_element(By.ID, 'content')
        textarea.send_keys('데이터 입력')
        time.sleep(5)
        btn = self.brower.find_element(By.ID, 'submit_btn')
        btn.click()




    def test_naver(self):
        '''https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com'''
        self.brower.get('https://nid.naver.com/nidlogin.login?mode=form&url=https%3A%2F%2Fwww.naver.com')

        #id
        id_textinput = self.brower.find_element(By.ID, 'id')
        id_textinput.send_keys('good_day')

        #비번
        pw_textinput = self.brower.find_element(By.ID, 'pw')
        pw_textinput.send_keys('4321')

        #버튼
        #
        btn_login = self.brower.find_element(By.ID, 'log.login')
        btn_login.click()  # 버튼 클릭
        pass

    @unittest.skip('test_selenium')
    def test_selenium(self):
        #FireFox 웹 드라이버 객체에게 Get을 통하여 네이버의 http요청을 하게 함.
        self.brower.get('http://127.0.0.1:8000/pybo/9/')
        print('self.brower.title:{}'.format(self.brower.title))
        self.assertIn('Pybo',self.brower.title)

        content_textarea=self.brower.find_element(By.ID,'content')
        content_textarea.send_keys('오늘은 아주 즐거운 금요일!')

        btn=self.brower.find_element(By.ID,'submit_btn')
        btn.click() # 버튼 클릭
        pass

    @unittest.skip('test_zip')
    def test_zip(self):
        ''' 여러개의 list를 묶어서 하나의 iterable객체로 다룰수 있게 한다. '''
        intergers = [1,2,3]
        letters   = ['a','b','c']
        floats    = [4.0,8.0, 10.0]
        zipped = zip(intergers,letters,floats)
        list_data = list(zipped)
        print('list_data:{}'.format(list_data))
        pass

    @unittest.skip('test_naver_stock')
    def test_naver_stock(self):
        '''주식 크롤링'''
        codes = {'삼성전자':'005930', '현대차':'005380'}
        for code in codes.keys():
            url = 'https://finance.naver.com/item/main.naver?code='
            #print(codes[code])
            url = url +str(codes[code])
            #print('url:{}'.format(url))

            response = requests.get(url)
            if 200 == response.status_code:
                html=response.text
                soup = BeautifulSoup(html, 'html.parser')
                # 제목
                price = soup.select_one('#chart_area div.rate_info div.today span.blind')
                #print('price:{}'.format(price.getText()))
                #today=price.select_one('.blind')
                print('today:{},{},{}'.format(code,codes[code],price.getText()))
            else:
                print('접속 오류 response.status_code:{}'.format(response.status_code))

        pass

    def call_slemdunk(self,url):
        response = requests.get(url)
        if 200 == response.status_code:
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            # 평점
            score = soup.select('div.list_netizen_score em')
            # 감상평
            review = soup.select('table tbody tr td.title')

            for i in range(0, len(score)):
                review_text = review[i].getText().split('\n')

                if len(review_text) > 2: #평점만 넣고 감상평 없는 경우 처리
                    tmp_text = review_text[5]
                else:
                    tmp_text = review_text[0]

                print('평점,감상평:{}#{}'.format(score[i].getText() , tmp_text ))

        else:
            print('접속 오류 response.status_code:{}'.format(response.status_code))

    @unittest.skip('slemdunk')
    def test_slemdunk(self):
        '''naver영화'''
        url = 'https://movie.naver.com/movie/point/af/list.naver?st=mcode&sword=223800&target=after&page='
        for i in range(1,4,1):
            self.call_slemdunk(url+str(i))

    @unittest.skip('slemdunk')
    def test_cgv(selfs):

        '''CGV http://www.cgv.co.kr/movies/?lt=1&ft=0'''
        url = 'http://www.cgv.co.kr/movies/?lt=1&ft=0'
        response=requests.get(url)

        if 200 == response.status_code:
            html=response.text
            #print('html:{}'.format(html))
            #box-contents
            soup=BeautifulSoup(html,'html.parser')
            #제목
            title = soup.select('div.box-contents strong.title')

            reserve = soup.select('div.score strong.percent span')
            #print('title:{}'.format(title))

            poster = soup.select('span.thumb-image img')

            for page in range(0,7,1):
                posterImg = poster[page]
                imgUrlPath = posterImg.get('src') #<img src='' /> 에 접근
                #print('imgUrlPath:{}'.format(imgUrlPath))
                print('title[page]:{},{},{}'.format(title[page].getText()
                                            ,reserve[page].getText()
                                            ,imgUrlPath
                                                 ))
                pass

        else:
            print('접속 오류 response.status_code:{}'.format(response.status_code))

    @unittest.skip('테스트 연습')
    def test_weather(self):
        ''' 날씨 '''
        # https://weather.naver.com/today/09545101
        now=datetime.datetime.now()
        #yyyymmdd hh:mm
        newDate=now.strftime('%Y-%m-%d %H:%M:%S') #2023-02-02 10:10:14
        print('='*35)
        print(newDate)
        print('=' * 35)

        #-------------------------------------------------
        naverWetherUrl = 'https://weather.naver.com/today/09440120'
        html=urlopen(naverWetherUrl)
        print('html:{}'.format(html))
        bsObject=BeautifulSoup(html,'html.parser')
        tmpes=bsObject.find('strong','current')
        print('서울 마포구 서교동 날씨:{}'.format(tmpes.getText()))

        print('test_weather')
        pass

