# !/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
from selectors import DefaultSelector,EVENT_WRITE,EVENT_READ

selector=DefaultSelector()
stopped=False
urls_todo={'/','/1','/2','/3','/4','/5','/6','/7','/8','/9',}

class Future:
    def __init__(self):
        self.result=None
        self._callbacks=[]

    def add_done_callback(self,fn):
        self._callbacks.append(fn)

    def set_result(self,result):
        self.result=result
        for fn in self._callbacks:
            fn(self)

    def __iter__(self):
        yield self
        return self.result


def connect(sock,address):
    f=Future()
    sock.setblocking(False)
    try:
        sock.connect(('example.com', 80))
    except BlockingIOError:
        pass

    def on_connected():
        f.set_result(None)

    selector.register(sock.fileno(), EVENT_WRITE, on_connected)
    yield from f
    selector.unregister(sock.fileno())

def read(sock):
    f = Future()

    def on_readable():
        f.set_result(sock.recv(4096))

    selector.register(sock.fileno(), EVENT_READ, on_readable)
    chunk = yield from f
    selector.unregister(sock.fileno())
    return chunk

def read_all(sock):
    response=[]
    chunk=yield from read(sock)
    while chunk:
        response.append(chunk)
        chunk=yield from read(sock)
    return b''.join(response)

class Crawler:
    def __init__(self,url):
        self.url = url
        self.response = b''

    def fetch(self):
        global stopped
        sock = socket.socket()
        yield from connect(sock,('example.com',80))
        get = 'GET {0} HTTP/1.0\r\nHost: example.com\r\n\r\n'.format(self.url)
        sock.send(get.encode('ascii'))
        self.response=yield from read_all(sock)
        urls_todo.remove(self.url)
        if not urls_todo:
            stopped=True


class Task:
    def __init__(self,core):
        self.core=core
        f=Future()
        f.set_result(None)
        self.step(f)

    def step(self,future):
        try:
            next_future=self.core.send(future.result)
        except StopIteration:
            return
        next_future.add_done_callback(self.step)

def loop(): #监听事件执行回掉
    while not stopped:
        events=selector.select()
        print(events)
        for event_key,event_mask in events:
            callback=event_key.data  #回掉函数的函数名
            callback()

if __name__ == '__main__':
    import time
    start=time.time()
    for url in urls_todo:
        crawer=Crawler(url)
        Task(crawer.fetch())
    loop()
    print(time.time()-start)