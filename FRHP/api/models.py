from django.db import models

# 房产信息表
class HouseInfo(models.Model):
    id = models.CharField(max_length=15, primary_key=True)  # 唯一标识符
    title = models.CharField(max_length=200)  # 标题
    administrative_district = models.CharField(max_length=15)  # 行政区
    city_planning_area = models.CharField(max_length=15)  # 城市规划区
    structure = models.CharField(max_length=5)  # 结构
    area = models.FloatField()  # 面积
    orientation = models.CharField(max_length=20)  # 朝向
    decoration = models.CharField(max_length=2)  # 装修
    house_type = models.CharField(max_length=4)  # 类型
    floor_height = models.CharField(max_length=3)  # 楼层高度
    floor_count = models.IntegerField()  # 楼层数
    price = models.FloatField()  # 价格
    # latitude_wgs = models.FloatField()  # 纬度
    # longitude_wgs = models.FloatField()  # 经度
    latitude_bd = models.FloatField()  # 纬度
    longitude_bd = models.FloatField()  # 经度

    def __str__(self):
        return self.title

# POI信息表
class POIInfo(models.Model):
    id = models.CharField(max_length=15, primary_key=True)  # 唯一标识符
    name = models.CharField(max_length=30)  # 名称
    administrative_district = models.CharField(max_length=15)  # 行政区
    first_tag = models.CharField(max_length=10)
    second_tag = models.CharField(max_length=10)
    latitude_bd = models.FloatField()  # 纬度
    longitude_bd = models.FloatField()  # 经度


    def __str__(self):
        return self.name