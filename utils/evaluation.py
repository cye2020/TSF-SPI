import numpy as np
import keras
from datetime import datetime


#===============================================================
def MSE(true, predict):
    """
    평균 제곱 오차 (MSE) 계산 함수

    Args:
        true: 실제 주가 데이터 (numpy array)
        predict: 예측 주가 데이터 (numpy array)

    Returns:
        평균 제곱 오차 (float)
    """
    return np.mean((true - predict)**2)

def MAE(true, predict):
    """
    평균 절대 오차 (MAE) 계산 함수

    Args:
        true: 실제 주가 데이터 (numpy array)
        predict: 예측 주가 데이터 (numpy array)

    Returns:
        평균 절대 오차 (float)
    """
    return np.mean(np.abs(true - predict))

def RMSE(true, predict):
    """
    루트 평균 제곱 오차 (RMSE) 계산 함수

    Args:
        true: 실제 주가 데이터 (numpy array)
        predict: 예측 주가 데이터 (numpy array)

    Returns:
        루트 평균 제곱 오차 (float)
    """
    return np.sqrt(MSE(true, predict))

def MAX_AE(true, predict):
    """
    최대 절대 오차 (MAX_AE) 계산 함수

    Args:
        true: 실제 주가 데이터 (numpy array)
        predict: 예측 주가 데이터 (numpy array)

    Returns:
        최대 절대 오차 (float)
    """
    return np.max(np.abs(true - predict))

def R2(true, predict):
    """
    결정 계수 (R^2) 계산 함수

    Args:
        true: 실제 주가 데이터 (numpy array)
        predict: 예측 주가 데이터 (numpy array)

    Returns:
        결정 계수 (float)
    """
    return 1 - np.sum((true - predict)**2) / np.sum((true - np.mean(true))**2)

def MAPE(true, predict):
    """
    평균 절대 백분율 오차 (MAPE) 계산 함수

    Args:
        true: 실제 주가 데이터 (numpy array)
        predict: 예측 주가 데이터 (numpy array)

    Returns:
        평균 절대 백분율 오차 (float)
    """
    return np.mean(np.abs((true - predict) / true)) * 100


def SMAPE(true, predict):
    """
    SMAPE (Symmetric Mean Absolute Percentage Error) 계산 함수

    Args:
        true: 실제 주가 데이터 (numpy array)
        predict: 예측 주가 데이터 (numpy array)

    Returns:
        SMAPE (float)
    """
    denominator = np.mean(np.abs(true) + np.abs(predict))
    return np.mean(np.abs(true - predict) / denominator) * 200


def evaluate(true, predict) -> dict:
    metrics = {}
    mse = MSE(true, predict)
    mae = MAE(true, predict)
    rmse = RMSE(true, predict)
    max_ae = MAX_AE(true, predict)
    r2 = R2(true, predict)
    mape = MAPE(true, predict)
    smape = SMAPE(true, predict)
    metrics['MSE'] = [round(mse, 2)]
    metrics['MAE'] = [round(mae, 2)]
    metrics['RMSE'] = [round(rmse, 2)]
    metrics['MAX_AE'] = [round(max_ae, 2)]
    metrics['R2'] = [round(r2, 2)]
    metrics['MAPE'] = [round(mape, 2)]
    metrics['SMAPE'] = [round(smape, 2)]
    return metrics
#===================================================================


def MSEs(true, predict):
    return np.average((true- predict)**2)

def MAEs(true, predict):
    return np.average(abs(true - predict))

def Absolute_Error_percentage(true, predict):
    return np.average(abs(true - predict) / true) * 100

def printResult(test_datelist, test_true, test_forecast, target, features):
    date_time = datetime.now()
    date = date_time.strftime("%Y%m%d")
    test_length = test_true[1:, -1].shape[0]
    test_result_list = []
    for i in range(test_length):
        test_result_list.append([test_datelist[- test_length + i], test_true[1:, -1][i], test_forecast[1:][:, -1][i]])
        
    test_yyyymm = []
    test_start_y = test_result_list[0][0].year
    test_end_y = test_result_list[-1][0].year
    test_start_m = test_result_list[0][0].month
    test_end_m = test_result_list[-1][0].month

    if (test_start_y == test_end_y):
        for i in range(test_start_m, test_end_m + 1):
            test_yyyymm.append(test_start_y * 100 + i)
    else:
        for i in range(test_end_y - test_start_y + 1):
            if (i == 0):
                for j in range(test_start_m, 13):
                    test_yyyymm.append((test_start_y + i) * 100 + j)
            elif (i == (test_end_y - test_start_y)):
                for j in range(1, test_end_m + 1):
                    test_yyyymm.append((test_start_y + i) * 100 + j)
            else:
                for j in range(1, 13):
                    test_yyyymm.append((test_start_y + i) * 100 + j)

    test_month_tf = {}
    errorRates = []
    for i in range(len(test_yyyymm)):
        test_month_tf[test_yyyymm[i]] = [0, 0]
    for i in range(len(test_result_list)):
        key = test_result_list[i][0].year * 100 + test_result_list[i][0].month
        test_month_tf[key][0] += test_result_list[i][1]
        test_month_tf[key][1] += test_result_list[i][2]
    for i in range(len(test_month_tf)):
        printYear = int(test_yyyymm[i] // 100)
        printMonth = int(test_yyyymm[i] % 100)
        printTrue = int(test_month_tf[test_yyyymm[i]][0])
        printForecast = round(test_month_tf[test_yyyymm[i]][1])
        printDiff = printTrue - printForecast
        errorRate = round(abs(printTrue - printForecast) / printTrue * 100, 2)
        print('[{0}년 {1}월] | 실제 코스피 지수: {2}원    | 예상 코스피 지수: {3}원       | 차이: {4}원       | 절대 오차율: {5}%'.format(printYear, printMonth, printTrue, printForecast, printDiff, errorRate))
        errorRates.append(errorRate)
        avg_errorRate = round(sum(errorRates)/len(errorRates), 2)
    print(f'평균 오차율: {avg_errorRate}')
    return avg_errorRate