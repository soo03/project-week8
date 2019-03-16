from stock.stock_model import StockModel
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
from fbprophet import Prophet
import plotly.offline as offline
import plotly.graph_objs as go


class StockModel:
    if __name__ == '__main__':
        model = StockModel('삼성전자')
        url = model.model()
        driver = webdriver.Chrome('chromedriver')
        driver.get(url)
        html = driver.page_source   # page_source는 페이지 소스를 전체 가져옴 (find_element는 필요한 부분만 찾아오는 것)
        soup = BeautifulSoup(html, 'html.parser')
        #print(soup.prettify())   # 실행창에 html 코드가 다 들어와있음 (한번 실행후 주석으로 막아둠)

        df = pd.DataFrame()

        for page in range(1, 10):   # 일단 10페이지까지 보기로 함
            page_url = '{url}&page={page}'.format(url=url, page=page) # url위에 페이지 번호가 다르게 나오므로 for문을 사용함
            df = df.append(pd.read_html(page_url, header=0)[0], ignore_index=True)
        df = df.dropna() # 결측값 있다면 제거
        print(df.head())

        df = df.rename(columns={'날짜':'date', '종가':'close', '전일비':'diff', '시가':'open',
                                '고가':'high', '저가':'low', '거래량':'volume'
                                })  # column 이름을 그래프 그릴때 한글이 깨지므로 영어로 바꿔줌
        # 원핫인코딩
        df[['close','diff','open','high','low','volume']] = df[['close','diff','open','high','low','volume']].astype(int)
        # date를 제외한 나머지들을 정수로 치환, date는 datetime형식으로 바꿈
        df['date'] = pd.to_datetime(df['date'])

        df = df.sort_values(by=['date'], ascending=True)
        print(df.head())

        







