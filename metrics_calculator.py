import os
import glob
import pandas as pd
import re
import matplotlib.pyplot as plt
import matplotlib.dates as mpl_dates
from datetime import datetime
from ggplot import *

# 1 = buy
# 0 = sell

def collect_metrics(folder_name):
    all_data = pd.read_csv(folder_name)

    #LABELS
    labels_arr = []
    for row in all_data.itertuples():
        if row.close - row.open > 0:
            labels_arr.append(1)
        else:
            labels_arr.append(0)
    labels = pd.DataFrame(labels_arr, columns=["label"])
    all_data["label"] = labels["label"]

    #PSAR
    myPsar = get_psar(all_data)
    all_data["psar"] = myPsar["psar"]

    #DATES
    dates_arr = []
    for row in all_data.itertuples():
        dates_arr.append(convert_to_date(row.date))
    dates = pd.DataFrame(dates_arr, columns=["date"])
    all_data["date"] = dates["date"]
    all_data.index = pd.to_datetime(all_data['date'])

    #MACD
    all_data["macd"] = get_macd(all_data["close"])

    '''
        #Stochastic
        all_data["stochastic"] = get_stochastic(all_data["close"], all_data["high"], all_data["low"])
        print all_data["stochastic"]
    '''
    all_data.to_csv("metrics_data.csv")

def get_macd(close_series):
    ema_12 = pd.ewma(close_series, span=17280)
    ema_26 = pd.ewma(close_series, span=37440)
    ema_diff = ema_12 - ema_26
    signal = pd.ewma(ema_diff, span=12960)
    macd_histogram = ema_diff - signal
    #creating lag
    macd_histogram = macd_histogram.iloc[1:]
    macd_histogram = macd_histogram.append(pd.DataFrame([0]),ignore_index=True)
    return macd_histogram.values

def get_psar(all_data, iaf = 0.02, maxaf = 0.2):
    length = len(all_data['date'])
    dates = list(all_data['date'])
    high = list(all_data['high'])
    low = list(all_data['low'])
    close = list(all_data['close'])

    psar = close[0:len(close)]
    psarbull = [0] * length
    psarbear = [0] * length

    bull = True
    af = iaf
    ep = low[0]
    hp = high[0]
    lp = low[0]

    for i in range(2,length):
        if bull:
            psar[i] = psar[i - 1] + af * (hp - psar[i - 1])
        else:
            psar[i] = psar[i - 1] + af * (lp - psar[i - 1])

        reverse = False

        if bull:
            if low[i] < psar[i]:
                bull = False
                reverse = True
                psar[i] = hp
                lp = low[i]
                af = iaf
        else:
            if high[i] > psar[i]:
                bull = True
                reverse = True
                psar[i] = lp
                hp = high[i]
                af = iaf

        if not reverse:
            if bull:
                if high[i] > hp:
                    hp = high[i]
                    af = min(af + iaf, maxaf)
                if low[i - 1] < psar[i]:
                    psar[i] = low[i - 1]
                if low[i - 2] < psar[i]:
                    psar[i] = low[i - 2]
            else:
                if low[i] < lp:
                    lp = low[i]
                    af = min(af + iaf, maxaf)
                if high[i - 1] > psar[i]:
                    psar[i] = high[i - 1]
                if high[i - 2] > psar[i]:
                    psar[i] = high[i - 2]

        if bull:
            psarbull[i] = psar[i]
        else:
            psarbear[i] = psar[i]

    for i in range(len(psar)):
        if psarbear[i] == 0:
            psar[i] = close[i] - psarbull[i]
        else:
            psar[i] = close[i] - psarbear[i]

    #creating lag
    psar.pop(0)
    psar.append(0)
    return pd.DataFrame(psar, columns=["psar"])


'''
def get_stochastic(recent_close, high_series, low_series):
    stochastic_arr = []
    low_14 = low_series.rolling('14D', min_periods=1).min()
    high_14 = high_series.rolling('14D', min_periods=1).max()
    mean_14 = recent_close.rolling('14D', min_periods=1).mean()
    stochastic_arr_raw = 100 * (mean_14 - low_14) / (high_14 - low_14)
    for val in stochastic_arr_raw:
        if (val > 80):
            stochastic_arr.append(1)
        else:
            stochastic_arr.append(0)
    return stochastic_arr
'''

def convert_to_date(date_int):
    yr = int(str(date_int)[0:4])
    mon = int(str(date_int)[4:6])
    day = int(str(date_int)[6:8])
    hr = int(str(date_int)[8:10])
    minute = int(str(date_int)[10:12])
    date = datetime(year=yr, month=mon, day=day, hour=hr, minute=minute),
    return date

if __name__ == '__main__':
    collect_metrics("BABA.csv")
