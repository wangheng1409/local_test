import numpy as np
# a=np.arange(15).reshape(3,5)
# print(a.itemsize,type(a))
#
# c=np.array([[1,2,3],[4,5,6]],dtype=complex)
# print(c)
#
#
# print(np.arange(10000).reshape(100,100))

# a=np.array([[1,2],[2,1]])
# b=np.array([[1,1,1],[1,1,1]])
# # print(a.dot(b))
# c=np.random.random((2,3))
# print(c)
#
#
# s=np.array([-1000])
# for i in s:
#     print(i**(1/3))


b=np.fromfunction(lambda x,y:2**x+y,(5,4),dtype=int)
print(b)
print(b.T,'\n',b.reshape(1,20),'\n',b.ravel())








