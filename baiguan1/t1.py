#coding=utf-8

# import psycopg2
# def main():
#   print ('starting...')
#   connection = psycopg2.connect(dbname="dev", user="root", password="big_one_112358", host="123.59.69.66", port='5432')
#   cursor = connection.cursor()
#   query_sql = """
#     select * from wuba.top_item limit 100
#   """
#   cursor.execute(query_sql)
#   con=cursor.fetchall()
#   print(len(con))
#   connection.close()
#   # query_result_pd.to_csv('query_result.csv', index=False, header=True, sep=',', encoding='utf8')
# if __name__ == '__main__':
#   main()

s=[[-1,0,1],[-1,2,-1],[1,0,-1]]
print([[int(a) for a in y.split('|')] for y in set('|'.join([str(y) for y in sorted(x)]) for x in s)])

print((lambda a,b: b if [b.append(sorted(x)) for x in s if sorted(x) not in b] else '')(s,[]))

t={k:v for k,v in zip([id(sorted(x)) for x in s],s)}.keys()

print(t)


from functools import reduce


info_list = [[1,2,3],[2,3,1],[2,3,4],[2,3,1],]
s = reduce(lambda x,y:x if sorted(y) in x else x + [y], [[], ]+s)
print (s)

# print([[], ] + info_list)
# print(info_list)


f=lambda i ,j :i if j==10 else f(i*2,j+1)
print(f(20,0))

import time
print(str(time.time()).replace('.','')[:13])
print(1513155423185)

x=12.2
print(id(x))

x=12.1
print(id(x))
x=12.2
print(id(x))

x=12.1
print(id(x))