import requests
import json
import time


def get_aicoiin_data(step):
    url = 'https://www.aicoin.cn/api/second/kline?'
    headers = {
        'Host': 'www.aicoin.cn',
        'Referer': 'https://www.aicoin.cn/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    postdata = {
        'symbol': 'zbusdtqc',
        'step': step
    }
    res = requests.get(url, headers=headers, params=postdata)
    data = json.loads(res.text)['data']
    t1 = data[0][0]
    timeArray = time.localtime(t1)
    startdata = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    print('数据开始日期：', startdata)
    print('数据结束日期：', time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(data[-1][0])))
    return data


if __name__ == '__main__':
    data = get_aicoiin_data(3600*4)
    #print(data)
