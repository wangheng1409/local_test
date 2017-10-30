import random
from MeituanSpider.util.MongoUtil import MongoUtil


def query_location():
    already = []
    handler = MongoUtil('lng-lat').handler
    location_list = handler.find({}, {'_id': 0})
    random_location_list = []
    for location in location_list:
        name = location['name']
        if name in already:
            continue
        already.append(name)
        if '单价' in name or '总价' in name or '佣金' in name:
            continue
        latitude = float(location['lat'])
        longitude = float(location['lng'])
        random_location_list.append({'latitude': latitude,
                                     'longitude': longitude,
                                     'name': name})
    random.shuffle(random_location_list)
    return random_location_list
