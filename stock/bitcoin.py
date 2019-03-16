from stock.stock_model import StockModel
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from fbprophet import Prophet
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")  # 어떤 사이트들은 웹 크롤링을 막으려고 중간에 크롤링을 중단시키는 소스를 만들어두는데 이를 무시하게 함


if __name__ == '__main__':
    driver = webdriver.Chrome('chromedriver')
    url = "https://bitcoincharts.com/charts/korbitKRW#rg730ztgSzm1g10zm2g25zv" # 비트코인차트 주소
    driver.get(url)
    xpath = """//*[@id="content_chart"]/div/div[2]/a"""
    # id=content_chart의 정규표현식, 그 안에 있는 div, 밑에 div의 세번째(인덱스=2) 밑에 속해 있는 a태그 안에 있는 링크를 모으려고 함
    variable = driver.find_element_by_xpath(xpath)
    driver.execute_script("return arguments[0].scrollIntoView();", variable)
    variable.click()
    # 그 메뉴가 보일 때까지 스크롤해서 내려가서 클릭하기
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    #print(soup.prettify())  # 실행해보면 크롬창에 숨겨져있던 테이블이 나타남, 한번 실행한 후에 주석으로 막아놓음

    # 그 페이지에서 F12로 소스이름 찾아보면 테이블 부분은 id=chart_table로 나옴
    table = soup.find_all('table', 'data')
    #table_div = soup.find(id="chart_table")
    #tables = table_div.find_all("table")
    print(table)

    df = pd.read_html(str(table))
    bitcoin = df[0]
    print(bitcoin.head())  # 컬럼명 확인(종가는 Close, 날짜는 Timestamp로 되어 있음
    bitcoin['Close'].plot(figsize=(12,6), grid=True) # 종가로 그래프 그려보기
    df = pd.DataFrame({'ds':bitcoin['Timestamp'], 'y':bitcoin['Close']})
    print(df)
    prophet = Prophet(yearly_seasonality=True, daily_seasonality=True)
    prophet.fit(df)
    future = prophet.make_future_dataframe(periods=30) # 미래값 예측
    forecast = prophet.predict(future)
    prophet.plot(forecast)









