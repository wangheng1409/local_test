import numpy as np
import pandas
from django.db import connection
from sklearn.metrics.pairwise import pairwise_distances
from sklearn import cross_validation as cv

import sys
sys.path.append("/data/www/chaomeng-bussiness/cron_jobs/")
sys.path.append("/data/www/chaomeng-bussiness-tobias/code/")

import settings
from sqlalchemy import create_engine

def get_barcode_store_ids():
    """
        find the barcode stores with active 500 sku
    """
    # bussiness_engine = create_engine(settings.BUSSINESS_DB_URL)
    # data = pandas.read_sql_query(
    #     '''
    #     SELECT
    #         summary.store_id,
    #         count(DISTINCT summary.item_id) as num_sku
    #     FROM
    #         summary_dailystoreitemsummary summary, (
    #             SELECT
    #                 distinct store_id as store_id
    #             FROM store_storeitem
    #             WHERE
    #                 length(receipt_item_id) = 13
    #         ) barcode_stores
    #     WHERE
    #         summary.store_id = barcode_stores.store_id
    #         AND summary.date >= '2016-08-01' AND summary.date < '2016-09-01'
    #     GROUP BY
    #         summary.store_id
    #     HAVING count(DISTINCT summary.item_id) > 500;
    #     ''', bussiness_engine)
    # return list(data['store_id'])
    return tuple([14, 62, 84, 91, 101, 104, 105, 111, 112, 117, 123, 134, 152, 158, 170, 243, 260, 263, 340, 358, 370, 401, 415, 427, 439, 440, 453, 459, 467, 479, 491, 498, 502, 503, 526, 535, 544, 552, 558, 562, 565, 632, 638, 649, 669, 687, 727, 728, 729, 733, 741, 774, 807, 888, 890, 915, 925, 926, 938, 948, 949, 954, 955, 972, 974, 999, 1005, 1006, 1008, 1009, 1010, 1011, 1012, 1013])

def build_item_percentage_table(stores):
    """
        1. compute item sales
        2. compute item sales percentage
    """
    bussiness_engine = create_engine(settings.BUSSINESS_DB_URL)
    total = pandas.read_sql_query(
        '''
        SELECT
            summary.store_id,  sum(sales) as sales
        FROM
            summary_dailystoreitemsummary summary
        WHERE
            summary.date >= '2016-08-01' AND summary.date < '2016-09-01' AND
            summary.store_id IN %(stores)s
        GROUP BY
            summary.store_id
        HAVING sum(num) > 10;
        ''', params={'stores': stores}, con=bussiness_engine)
    total_dict = {}
    for _, row in total.iterrows():
        total_dict[row.store_id] = row.sales

    data = pandas.read_sql_query(
        '''
        SELECT
            summary.store_id, summary.item_id, sum(sales) as sales
        FROM
            summary_dailystoreitemsummary summary, store_storeitem items
        WHERE
            summary.item_id = items.id AND
            summary.date >= '2016-08-01' AND summary.date < '2016-09-01' AND
            items.receipt_item_id IS NOT NULL AND length(items.receipt_item_id) = 13 AND
            summary.store_id IN %(stores)s
        GROUP BY
            summary.store_id, summary.item_id
        HAVING sum(num) > 10 AND sum(sales) > 10;
        ''', params={'stores': stores}, con=bussiness_engine)
    per = []

    for _, row in data.iterrows():
        per.append(float(row.sales) / total_dict[row.store_id])
    data['per'] = per
    data.to_sql('store_item_matrix', bussiness_engine, if_exists='replace')

#### compute per tables
# stores = get_barcode_store_ids()
# print build_item_percentage_table(stores)


# df = pandas.read_sql_query(
#     '''
#     SELECT
#         s.store_id, s.k as tag, count(s.k) as num_sku, sum(s.num) as num
#     FROM (
#         SELECT
#             items.store_id, unnest(keywords) as k, item_num.num
#         FROM
#             store_storeitem items, (
#                 SELECT
#                     summary.store_id, summary.item_id, sum(num) as num
#                 FROM
#                     summary_dailystoreitemsummary summary
#                 WHERE
#                     summary.date >= '2016-08-01' AND summary.date < '2016-09-01' AND
#                     summary.store_id IN (23,243,552,440,370,888,502,733,949,729,955,926,638,81,954,62,565,131,972,544,562,439,91,69,974,774,46,498,415,143,125,727,184,123,215,45,501,358,807,208,503,345,84,463,263,170,486,728,669,55,890,1005,152,434,321,14,915,479)
#                 GROUP BY
#                     summary.store_id, summary.item_id
#                 HAVING sum(num) > 10
#             ) item_num
#         WHERE
#             items.store_id = item_num.store_id AND
#             items.id = item_num.item_id
#     ) s
#     RIGHT JOIN
#         standard_standardtag tags
#     ON
#         s.k = tags.tag AND (tags.type = 'brand' or tags.type = 'series')
#     GROUP BY s.store_id, s.k
#     HAVING count(s.k) > 0
#     ORDER BY count(s.k) DESC;
#     ''', bussiness_engine)
# df.to_sql('store_item_matrix', bussiness_engine, if_exists='replace')


##################
##################
##################
##################
bussiness_engine = create_engine(settings.BUSSINESS_DB_URL)
df = pandas.read_sql_query('''
    SELECT
        matrix.*,
        item.receipt_item_id as barcode
    FROM
        store_item_matrix matrix,
        store_storeitem item
    WHERE
        item.id = matrix.item_id;
    ''', bussiness_engine, index_col=['index'])
n_stores = df.store_id.unique().shape[0]
n_barcodes = df.barcode.unique().shape[0]

store_ids = dict(zip(df.store_id.unique(), range(len(df.store_id.unique()))))
barcode_ids = dict(zip(df.barcode.unique(), range(len(df.barcode.unique()))))

inverted_store_ids = dict(zip(range(len(df.store_id.unique())), df.store_id.unique()))
inverted_barcode_ids = dict(zip(range(len(df.barcode.unique())), df.barcode.unique()))
print 'Number of stores = %d, Number of barcodes = %d' % (n_stores, n_barcodes)
train_data, test_data = cv.train_test_split(df, test_size=0.25)

train_data_matrix = np.zeros((n_stores, n_barcodes))
for line in train_data.itertuples():
    train_data_matrix[store_ids[line.store_id], barcode_ids[line.barcode]] = round(line.per * 100.0, 2)

test_data_matrix = np.zeros((n_stores, n_barcodes))
for line in test_data.itertuples():
    test_data_matrix[store_ids[line.store_id], barcode_ids[line.barcode]] = round(line.per * 100.0, 2)

user_similarity = pairwise_distances(train_data_matrix, metric='cosine')
item_similarity = pairwise_distances(train_data_matrix.T, metric='cosine')

def predict(ratings, similarity, type='user'):
    if type == 'user':
        mean_user_rating = ratings.mean(axis=1)
        ratings_diff = (ratings - mean_user_rating[:, np.newaxis])
        pred = mean_user_rating[:, np.newaxis] + similarity.dot(ratings_diff) / np.array([np.abs(similarity).sum(axis=1)]).T
    elif type == 'item':
        pred = ratings.dot(similarity) / np.array([np.abs(similarity).sum(axis=1)])
    return pred

item_prediction = predict(train_data_matrix, item_similarity, type='item')
user_prediction = predict(train_data_matrix, user_similarity, type='user')

from sklearn.metrics import mean_squared_error
from math import sqrt
def rmse(prediction, ground_truth):
    prediction = prediction[ground_truth.nonzero()].flatten()
    ground_truth = ground_truth[ground_truth.nonzero()].flatten()
    return sqrt(mean_squared_error(prediction, ground_truth))

print 'User-based CF RMSE: ' + str(rmse(user_prediction, test_data_matrix))
print 'Item-based CF RMSE: ' + str(rmse(item_prediction, test_data_matrix))

sparsity=round(1.0-len(df)/float(n_stores*n_barcodes),3)
print 'The sparsity level is ' +  str(sparsity*100) + '%'

import scipy.sparse as sp
from scipy.sparse.linalg import svds

#get SVD components from train matrix. Choose k.
u, s, vt = svds(train_data_matrix, k = 20)
s_diag_matrix=np.diag(s)
X_pred = np.dot(np.dot(u, s_diag_matrix), vt)
print 'User-based CF MSE: ' + str(rmse(X_pred, test_data_matrix))

from operator import itemgetter
def out_recommendation_result(result_matrix):
    stores = []
    barcode = []
    per = []
    for store_id in store_ids.keys():
        store_barcodes = set(df.loc[df['store_id']==store_id].barcode)
        store_barcodes_idx = set()
        for b in store_barcodes:
            store_barcodes_idx.add(barcode_ids[b])
        row = result_matrix[store_ids[store_id]]
        for i in range(len(row)):
            if i not in store_barcodes_idx:
                stores.append(store_id)
                barcode.append(inverted_barcode_ids[i])
                per.append(row[i])
    out_df = pandas.DataFrame()
    out_df['store_id'] = stores
    out_df['barcode'] = barcode
    out_df['per'] = per
    out_df.to_sql('store_item_rec_result', bussiness_engine, if_exists='replace')

out_recommendation_result(X_pred)