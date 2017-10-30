# !/usr/bin/env python
# -*- coding:utf-8 -*-

async def say_hello():
    print('in say_hello')
    return 'Hello'

async def say_word():
    print('in say_word')
    return 'Word'



async def say_helloword():
    print('in say_helloword')
    value=await say_hello()+ await say_word()
    return value

import uvloop
import asyncio

loop=asyncio.get_event_loop()

asyncio.wait([say_hello(),say_word()])
#fs = {ensure_future(f, loop=loop) for f in set(fs)}
#Returns two sets of Future: (done, pending).
#Usage:done, pending = yield from asyncio.wait(fs)
#如果设置timeout，就算Future没有执行完也不会产出TimeoutError




asyncio.as_completed([say_hello(),say_word()])
#todo = {ensure_future(f, loop=loop) for f in set(fs)}
#Return an iterator whose values are coroutines，即 值是协程的可叠带对象
#会按照完成的顺序得到结果
#如果设置timeout,当Future没有执行完，将会reaise TimeoutError

asyncio.gather([say_hello(),say_word()])

'''
    for arg in set(coros_or_futures):
        if not futures.isfuture(arg):
            fut = ensure_future(arg, loop=loop)'''

'''
Return a future aggregating results from the given coroutines
    or futures，根据传进来的协程或者Future,返回聚合后的Future result'''

'''
All futures must share the same event loop'''
#如果全部执行成功，就会返回一个不一定按顺序的结果list，如果有异常也会收集异常结果










