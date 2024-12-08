import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA

df = pd.read_excel(r'C:/Users/Heikki/Documents/Portfolio/Data/Online Retail.xlsx')

df.head()
df.columns
df. shape
df.dtypes
df.info()
np.sum(df.isnull().any(axis=1))
print('length of data is', len(df))
print('Count of columns in the data is:  ', len(df.columns))
print('Count of rows in the data is:  ', len(df))
df.duplicated().sum()


                   
