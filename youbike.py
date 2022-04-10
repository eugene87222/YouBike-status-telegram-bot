# -*- coding: utf-8 -*-
import json
import requests
from math import radians, cos, sin, asin, sqrt


def get_all_stations(youbike_type=1):
    url = f'https://apis.youbike.com.tw/api/front/station/all?lang=en&type={youbike_type}'
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'}
    res = requests.get(url, headers=headers)
    stations = json.loads(res.text)['retVal']
    return stations


def get_radius(user_id):
    radius_dict = json.load(open('radius.json', 'r', encoding='utf-8'))
    return radius_dict.get(str(user_id), radius_dict['default'])


def save_radius(user_id, radius):
    radius_dict = json.load(open('radius.json', 'r', encoding='utf-8'))
    radius_dict[str(user_id)] = radius
    json.dump(radius_dict, open('radius.json', 'w', encoding='utf-8'))


def distance(lat1, lon1, lat2, lon2): 
    lon1 = radians(lon1)
    lat1 = radians(lat1)
    lon2 = radians(lon2)
    lat2 = radians(lat2)
    dlon = lon2 - lon1  
    dlat = lat2 - lat1 
    dis = 6371 * 2 * asin(sqrt(sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2))
    return dis


def generate_formatted_output(results):
    output = []
    for s in results:
        (s, dis, lat, lng) = s
        station_name = s['name_tw']
        dist = s['district_tw']
        addr = s['address_tw']
        total_space = s['parking_spaces']
        avail_space = s['available_spaces']
        empty_space = s['empty_spaces']
        update_time = s['updated_at']

        res = f'*{station_name}*'
        if dis:
            res += f' ({dis:.1f}m)'
        res += f'\n[See on Google Map](https://www.google.com/maps/search/?api=1&query={lat:.6f},{lng:.6f})\n'
        res += f'地點：{dist} - {addr}\n'
        res += f'可借/總數：*{avail_space}/{total_space}*\n'
        res += f'_updated at {update_time}_'
        output.append(res)
    return '\n\n\n'.join(output)


def get_status_by_coor(stations, user_id, coor):
    target_s = []
    radius = get_radius(user_id)
    for s in stations:
        try:
            dis = distance(coor['latitude'], coor['longitude'], float(s['lat']), float(s['lng']))
            if dis <= radius/1000:
                target_s.append((s, dis*1000, float(s['lat']), float(s['lng'])))
        except:
            continue
    if len(target_s) == 0:
        return f'方圓 {radius} 公尺內沒有站耶，呵呵呵'
    else:
        target_s = sorted(target_s, key=lambda t: t[1])
        if len(target_s) > 5:
            target_s = target_s[:5]

    return generate_formatted_output(target_s)


def get_status_by_kw(stations, kw_list):
    target_s = []
    for s in stations:
        info = s['name_tw'] + ',' + s['district_tw'] + ',' + s['address_tw']
        if all(kw in info for kw in kw_list):
            target_s.append((s, None, float(s['lat']), float(s['lng'])))
    if len(target_s) == 0:
        return '找不到東西，你是不是有打錯字'
    elif len(target_s) > 10:
        return '關鍵字打太少了啦，超過 10 筆搜尋結果，Telegram 有單一訊息字數上限'

    return generate_formatted_output(target_s)
