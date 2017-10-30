import pymongo

client=pymongo.MongoClient('mongodb://root:Baiguan2016@60.205.152.167:3717')
database=client.boss
col=database.boss_company.find({},{'_id':0,'ts':0,'ts_string':0})
f1=open('boss_company.csv','w')
f1.close()
with open('boss_company.csv','w',encoding='utf8') as f:
    for company in col:
        f.write('\t'.join([
            company['company'], #公司名
            company['company_id'],#公司id
            company['industry'],#行业
            company['total_job'],#职位总数
            company['people'],#公司人数
            company['total_boss'],#boss数量
            company['wheel'],#第几轮融资
            company['com'], #公司网址
        ])+'\n')

