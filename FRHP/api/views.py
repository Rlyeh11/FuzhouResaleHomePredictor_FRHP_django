import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import joblib
from api.utils.module_features_clear import *
import api.utils.map_position_transform as mpt
import pandas as pd

# encoding:utf-8
from tqdm import tqdm
import os

print(os.path.abspath(__file__))

model_date = '2024_03_19 13_53_46'
kmeans = joblib.load(f'api/model/kmeans_{model_date}_GBRT.model')
GBRT= joblib.load(f'api/model/GBRT/GBRT_{model_date}.model')
encoder = joblib.load('api/model/encoder.pkl')

# Create your views here.
@csrf_exempt
def predict_houseprice(request):
    if request.method == 'GET':
        return JsonResponse({'status': '200', 'msg': 'get request sent successfully'})
    elif request.method == 'POST':
        # 处理 POST 请求的表单数据
        # 例如，如果 POST 请求中包含名为 'data' 的字段，你可以这样获取它的值
        data = json.loads(request.body.decode('utf-8'))  # 解析 JSON 数据
        features = data.get('data', None)
        if features is not None:
            try:
                [lon, lat] = [features.get('longitude'), features.get('latitude')]
                # [lon, lat] = mpt.bd09_wgs84(features.get('longitude'), features.get('latitude'))
                features['longitude'] = lon
                features['latitude'] = lat
                features['house_area'] = float(features['house_area'])
                features_df = pd.DataFrame(features)
                # print(features_df.columns)
                features_df.columns = ['行政区', '房屋类型', '房屋装修', '房屋结构', '房屋朝向', '房屋面积', '楼层数', '楼层位置',
                                                   '经度_wgs', '纬度_wgs']
                # tags = ['中餐厅', '小吃快餐店', '酒吧', '购物中心', '百货商场', '便利店', '市场', '洗衣店', '宠物服务', '公园', '景点', '文物古迹', '农家院', '电影院', 'ktv', '休闲广场', '体育场馆', '健身中心', '中学', '小学', '幼儿园', '综合医院', '诊所', '药店', '急救中心', '医疗保健', '地铁站', '公交车站', '停车场', '银行', '信用社', '公司', '园区']
                KDTrees = joblib.load(r'api/model/KDtrees.pkl')
                trees = KDTrees['trees']
                gdfs = KDTrees['gdfs']
                for category, group_gdf in tqdm(gdfs.items(), total=len(gdfs)):
                    col = str(category) + '_1.5km'
                    features_df[col] = 0
                for index, rows in tqdm(features_df.iterrows(), total=len(features_df)):
                    for category, group_gdf in gdfs.items():
                        # 通过R树 找寻最近的POI点
                        nearest_poi = find_nearest_poi(rows['经度_wgs'], rows['纬度_wgs'], trees[category], group_gdf)
                        # 计算最近POI距离
                        distance = int(
                            calculate_distance(rows['经度_wgs'], rows['纬度_wgs'], nearest_poi['longitude_wgs'],
                                               nearest_poi['latitude_wgs']))
                        if distance <= 1500:
                            col = str(category) + '_1.5km'
                            features_df.loc[index, col] = 1
                module_features_without_position, p = get_X_p(features_df, encoder)
                clusters = kmeans.predict(p)
                pred = [GBRT[cluster].predict(module_features_without_position.iloc[i].values.reshape(1, -1))[0] for i, cluster in
                        enumerate(clusters)]

            except KeyError as e:
                print(e)
                return JsonResponse({'status': '200', 'msg': 'data not valid'})
            return JsonResponse({'status': '200', 'msg': 'request post successfully', 'data': pred[0]})
        else:
            return JsonResponse({'status': '400', 'msg': 'data is missing in the request'})

    return JsonResponse({'status': '404', 'msg': 'error'})
