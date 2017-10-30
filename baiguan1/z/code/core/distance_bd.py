import math
class Point:
   def  __init__(self,lat,lng):
        self.lat = float(lat)
        self.lng = float(lng)


def lw(a, b, c):
    a = max(a,b)
    a = min(a,c)
    return a

def ew(a, b, c):
    
    while a > c:
        a -= c - b
    while a < b:
        a += c - b
    return a
        

def oi(a):
    return math.pi * a / 180

def Td(a, b, c, d): 
    return 6370996.81 * math.acos(math.sin(c) * math.sin(d) + math.cos(c) * math.cos(d) * math.cos(b - a))

def distance_compute(a, b):
    if not a or not b: 
        return 0;
    a.lng = ew(a.lng, -180, 180);
    a.lat = lw(a.lat, -74, 74);
    b.lng = ew(b.lng, -180, 180);
    b.lat = lw(b.lat, -74, 74);
    return Td(oi(a.lng), oi(b.lng), oi(a.lat), oi(b.lat))

def distance_bd(a, b):
    point_a = Point(a['lat'],a['lng'])
    point_b = Point(b['lat'],b['lng'])
    c = distance_compute(point_a, point_b);
    return c

