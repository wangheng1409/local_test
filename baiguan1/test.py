# # 计算12000个实验，每次实验成功10%，一共需要多少次
# f = lambda i, j: f(i * 0.9, j + 1) if i > 10 else j
# print(f(12000, 0))
#
# # 随机产生32位字母和字符串的组合
# import random
#
# print(''.join(
#     map(lambda i: chr(random.randint(97, 122)) if random.randint(1, 4) in [1, 2] else str(random.randint(0, 9)),
#         range(32))))
#
# # 二分升序查找，有返回元素，没有返回False
# f = lambda li, s: li[int(len(li) / 2)] if li[int(len(li) / 2)] == s else (
# False if len(li) < 2 else f(li[:int(len(li) / 2)], s) if s < li[int(len(li) / 2)] else f(li[int(len(li) / 2):], s))
# print(f([-34, -2, 0, 3, 8, 9, 34], 34))
#
# #lambda表达式实现斐波那契数列
# f = lambda li, s: f(li if not li.append(li[-1] + li[-2]) else [],s) if len(li)<s else li
# print(f([0, 1], 10))
# from datetime import timedelta, date
# i=3
# day = str(date.today() - timedelta(days=i))
# print(day)
'1500280361030'
'1500281913537'
# import time
# print(str(time.time()).replace('.','')[:13])
# s= "快件 北京航"
# # w=s.split(' ')
# # print(w)

# s={'男鞋': 57739, '食品酒水': 7459, '家居家纺': 47287, '美妆个护': 26081, '唯品国际': 4977, '家用电器': 3924, '家具家装': 15483, '女鞋': 104431, '女装': 344641, '运动户外': 85937, '男装': 192420, '男女内衣': 75606, '手表配饰': 92491, '箱包皮具': 131549, '母婴': 113330, '唯品·奢': 3850, '手机数码': 4320}
# t={'男鞋': 111053, '食品酒水': 12145, '家居家纺': 87950, '家用电器': 5727, '家具家装': 29590, '美妆个护': 42579, '女装': 791775, '男女内衣': 181158, '运动户外': 132250, '唯品国际': 12008, '母婴': 147345, '男装': 337088, '唯品·奢': 8095, '箱包皮具': 263177, '手表配饰': 148029, '手机数码': 6749, '女鞋': 279403}
#
# for a,b in s.items():
#     print(a.center(10,' '),str(b).center(10,' '),str(t[a]).center(10,' '))
#
# from collections import deque
# data = deque([1,2])
# sql_tpl = "insert xxxxx"
# cnt = 1
# while data:
#     # sql = sql_tpl.format(data.popleft())
#     # conn.execute(sql)
#     # if cnt == 0 or not data:
#     #     conn.commit()
#     #     cnt = 10000
#     # cnt -= 1
#     data.popleft()
#     cnt-=1
#     if cnt == 0 or not data:
#         print(1)
#         cnt=2



# s='<dd class=\"basicInfo-item value\">\n申积军，王燕，刘洋，王艳<sup>[2]</sup><a class=\"sup-anchor\" name=\"ref_%5B2%5D_10548716\"> </a >\n</dd>'
# s=s.split('>')[1].split('<')[0]
# print(s)
