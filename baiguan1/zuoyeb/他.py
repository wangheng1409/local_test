def f(name=None,**kwargs):
    l=[]
    l.append(name)
    if kwargs:
        for k,v in kwargs.items():
            l.append('{}:{}'.format(k,v))
    print(l)
    l=str(l)
    print(type(l),l)
    l.strip('[]')
    print(type(l), l)
    l=l.replace("','",',')
    print(type(l), l)
    return l

f('abc')
