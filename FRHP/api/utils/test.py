import geopandas as gpd
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.neighbors import KDTree
from shapely.geometry import Point
import joblib

kmeans = joblib.load('./best_model/kmeans/kmeans_2024_03_19 13_53_46_GBRT.model')

# 假设你已经有了一个训练好的KMeans模型，名为kmeans
centers = kmeans.cluster_centers_
print("聚类中心:\n", centers)
labels = kmeans.labels_
print("样本聚类标签:", labels)
print(len(centers))
print(len(labels))
# 119.35514917708481
# 25.41289883718246

# 119.77641852890491
# 26.4129011327927
import matplotlib.pyplot as plt

# 创建一个图形和坐标轴
fig, ax = plt.subplots()
map_image_path = './fz_background.webp'
# 将图片设置为坐标轴的背景
img = plt.imread(map_image_path)
ax.imshow(img, extent=[min(centers[:, 0])-0.5, max(centers[:, 0])+0.87, min(centers[:, 1])-0.2, max(centers[:, 1])+0.35],
          aspect='auto', transform=ax.transAxes)
# 假设数据集X是二维的
# plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis', marker='o')
# ax.scatter(centers[:, 0], centers[:, 1], s=1, c='red', marker='x')
ax.scatter([25.41289883718246, 26.4129011327927], [119.35514917708481, 119.77641852890491], s=10, c='red', marker='x')

# ax.axis('off')
# 设置图片在坐标轴中的布局
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
fig.patch.set_facecolor('none')

plt.title('KMeans聚类结果')
plt.show()