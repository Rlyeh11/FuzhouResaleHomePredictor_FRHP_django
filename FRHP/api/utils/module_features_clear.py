import time
import warnings

import joblib
import pandas as pd
import numpy as np
import os
from shapely.geometry import Point
import geopandas as gpd
from sklearn.neighbors import KDTree
from sklearn.preprocessing import OneHotEncoder
from tqdm import tqdm

warnings.simplefilter('ignore')


def one_hot_toward(data: pd.DataFrame):
    one_hot_data = pd.DataFrame(np.zeros((len(data.index), 8), dtype=int))
    dir = ['东', '南', '西', '北', '东北', '东南', '西南', '西北']
    one_hot_data.columns = ['房屋朝向_' + col for col in dir]
    one_hot_data.index = data.index
    for ind in data.index:
        tmp = data['房屋朝向'][ind].split(' ')
        for cx in tmp:
            one_hot_data['房屋朝向_' + cx][ind] = 1
    return one_hot_data


def get_X_p(X, encoder):
    house_toward = one_hot_toward(X[['房屋朝向']])
    X.drop(columns=['房屋朝向'], axis=1, inplace=True)
    X_categorical = X.select_dtypes(include=['object'])  # 选择 object 类型的列
    """通过使用对Object类型的筛选 过滤掉数字类型以及已经转换为dummies的数据列"""
    # 对 object 类型的列进行独热编码
    X_categorical = X_categorical[['行政区','房屋结构', '房屋装修', '房屋类型', '楼层位置']]
    X_encoded = encoder.transform(X_categorical)
    X_encoded = X_encoded.astype(int)
    # 将编码后的稀疏矩阵转换为DataFrame并设置列名
    encoded_columns = encoder.get_feature_names_out(input_features=X_categorical.columns)
    X_encoded_dense = X_encoded.toarray()
    X_encoded_df = pd.DataFrame(X_encoded_dense, columns=encoded_columns)
    # 将编码后的数据与原数据集合并
    X = pd.concat([X.drop(X_categorical.columns, axis=1), X_encoded_df], axis=1)
    X = pd.concat([X, house_toward], axis=1)
    # 地理位置数据
    p = X[['纬度_wgs', '经度_wgs']]
    X.drop(['经度_wgs', '纬度_wgs'], axis=1, inplace=True)
    return X, p



def find_nearest_poi(target_lon, target_lat, tree, gdf):
    distances, indices = tree.query([(target_lon, target_lat)], k=1)
    nearest_poi = gdf.iloc[indices[0]]
    return nearest_poi


def calculate_distance(lon1, lat1, lon2, lat2):
    # 使用标准经纬度坐标系计算两点之间的距离
    # 以下是 haversine 公式的代码
    from math import radians, sin, cos, sqrt, atan2
    # 将经度和纬度转换为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine 公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371000 * c  # 地球半径为6371公里，乘以1000转换为米
    return distance
