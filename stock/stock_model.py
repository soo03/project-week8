import pandas as pd

class StockModel:
    def __init__(self, item_name):
        self.item_name = item_name

    def model(self):
        #code_df = pd.read_html("http://kind.krx.co.kr/disclosureSimpleSearch.do", header="0")[0]  # 업체별 종목코드 모아놓은 페이지
        #code_df.종목코드 = code_df.종목코드.map('{:06d}'.format) # 종목코드 6자리
        #code_df = code_df.rename(columns={'회사명: ': 'name', '종목코드': 'code'})
        #print(code_df.head())
        #self.code = code_df.query("name=='{}'".format(self.item_name))['code'].to_string(index=False)
        code = '005930' # 삼성전자 종목코드로 일단 수동으로 넣어봄
        url = "https://finance.naver.com/item/sise_day.nhn?code={code}".format(code=code)
        print("요청 url = {}".format(url))
        return url