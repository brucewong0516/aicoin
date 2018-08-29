import requests
import json
import re
import pymongo
import time


class Aicoin_period_chart_api(object):
    def __init__(self):
        self.__exchange_list_url = 'https://www.aicoin.cn/chart/59D56005'
        self.__period_chart_url = 'https://www.aicoin.cn/chart/api/data/period?'
        self.__periodhistory_chart_url = 'https://www.aicoin.cn/chart/api/data/periodHistory?'
        self.headers = {
            'Host': 'www.aicoin.cn',
            'Referer': 'https://www.aicoin.cn/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
            }
        self.postdata = {'symbol': '', 'step': ''}

    def get_exchange_list_data(self):
        try:
            res = requests.get(self.__exchange_list_url, headers=self.headers)
            window_COINS_pattern = re.compile('window.COINS = \[.*?\];', re.S)
            dicts_pattern = re.compile('{.*?}', re.S)
            window_COINS = re.findall(window_COINS_pattern, res.text)[0]
            dicts = re.findall(dicts_pattern, window_COINS)
            market_list = []
            for dict in dicts:
                new_dict = json.loads(dict)
                market_list.append(new_dict)
            client = pymongo.MongoClient('localhost', 27017)
            db = client['market_list']
            sheet = db['sheet']
            sheet.insert_many(market_list)
            print('market_list已存进数据库！')
        except requests.RequestException:
            print('获取market_list时网络出现错误！')
    # 获取交易所列表，交易所数据，交易对名称

    def get_period_chart_data(self, symbol, step):
        try:
            #self.headers['Referer'] = 'https://www.aicoin.cn/chart/'
            self.postdata['symbol'] = symbol
            self.postdata['step'] = step
            res1 = requests.get(self.__period_chart_url, headers=self.headers, params=self.postdata)
            period_data = list(reversed(json.loads(res1.text)['data']))
            self.postdata['count'] = json.loads(res1.text)['count']
            self.headers['Origin'] = 'https://www.aicoin.cn'
            for i in range(1, 100000):
                self.postdata['times'] = str(i)
                res2 = requests.post(self.__periodhistory_chart_url, headers=self.headers, params=self.postdata)
                period_history_data = json.loads(res2.text)
                if len(period_history_data) == 0:
                    break
                else:
                    period_data = period_data + list(reversed(period_history_data))
                time.sleep(0.1)
            t1 = period_data[0][0]
            t2 = period_data[len(period_data) - 1][0]
            timeArray1 = time.localtime(t1)
            timeArray2 = time.localtime(t2)
            start_data = time.strftime("%Y--%m--%d %H:%M:%S", timeArray2)
            end_data = time.strftime("%Y--%m--%d %H:%M:%S", timeArray1)
            print('数据长度：', len(period_data))
            print('数据开始日期：', start_data)
            print('数据结束时间：', end_data)
            return period_data
        except requests.RequestException:
            print('获取', symbol, '时网络出现错误！步长为：', step)
            return []
    # 此函数可获取一个交易对的所有历史价格数据(前提是step是固定的)
    # symbol为交易对名称(若需要查看所有的交易对名称，可使用get_exchange_list_data()函数来获取)
    # step为步长（可选60,300,900,1800,3600,14400,43200,86400,604800,2592000）
    # 代表1分钟，5分钟，15分钟，30分钟，1小时，4小时，12小时，24小时，1周，1月
    # 返回为一个列表(已按时间戳从小到大的顺序排列好)


if __name__ == '__main__':
    # 调用实例
    period_data = Aicoin_period_chart_api().get_period_chart_data('okexbtcusdt', 3600)
