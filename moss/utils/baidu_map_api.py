# -*- coding: utf-8 -*-
# @Time    : 2023/5/5 下午5:12
# @Author  : Su Yang
# @File    : baidu_map_api.py
# @Software: PyCharm 
# @Comment :
import os
import requests
import dotenv

dotenv.load_dotenv("../../.env")


def district_place_search(query: str, region: str) -> dict:
    """
    行政区划分检索
    详细信息见: https://lbsyun.baidu.com/faq/api?title=webapi/guide/webservice-placeapi/district
    Args:
        query: 用户检索需求
        region: 区域

    Returns:
        检索结果列表
    """
    # 接口地址
    url = "https://api.map.baidu.com/place/v2/search"

    params = {
        "query": query,
        "region": region,
        "page_size": 5,
        "city_limit": 'true',
        "output": "json",
        "scope": 2,
        "ak": os.environ['BAIDU_MAP_API_AK'],
    }
    response = requests.get(url=url, params=params)
    res: dict = response.json() if response else None
    return res


def circle_place_search(query: str, user_location: str) -> dict:
    """
    圆形区域检索
    详细信息见: https://lbsyun.baidu.com/faq/api?title=webapi/guide/webservice-placeapi/circle
    Args:
        query: 用户检索需求
        user_location: 区域

    Returns:
        检索结果列表
    """
    url = "https://api.map.baidu.com/place/v2/search"

    params = {
        "query": query,
        "location": user_location,
        "page_size": 5,
        "radius": "1500",
        "output": "json",
        "scope": 2,
        "ak": os.environ['BAIDU_MAP_API_AK'],
    }
    response = requests.get(url=url, params=params)
    res: dict = response.json() if response else None
    return res


def regional_search_res2str(res: dict) -> str:
    """
    将区域检索查询到的结果处理成字符串
    Args:
        res: 查询结果

    Returns:
        查询结果的字符串
    """
    output = ''
    if res is not None:
        if res.get('status') == 0:
            for i, result in enumerate(res.get('results')):
                output += f'{i + 1}.名称：' + result.get('name') + \
                          ' 地址：' + result.get('address') + '\n'
            return output
        else:
            return res.get('message')
    else:
        return ''


def address2location(address: str) -> str:
    """
    通过地址获取经纬度
    Args:
        address: 地址

    Returns:
        str：'{lat},{lng}'
    """
    # 接口地址
    url = "https://api.map.baidu.com/geocoding/v3"

    params = {
        "address": address,
        "output": "json",
        "ak": os.environ['BAIDU_MAP_API_AK'],
    }

    response = requests.get(url=url, params=params)
    res: dict = response.json() if response else None
    if res is not None:
        if res.get('status') == 0:
            return str(res.get('result').get('location').get('lat')) + \
                ',' + \
                str(res.get('result').get('location').get('lng'))
        else:
            return ''
    else:
        return ''


def location2address(location: str) -> dict:
    # 接口地址
    url = "https://api.map.baidu.com/reverse_geocoding/v3"

    params = {
        "ak": os.environ['BAIDU_MAP_API_AK'],
        "output": "json",
        "location": location,

    }

    response = requests.get(url=url, params=params)
    return response.json() if response else None


def address2adcode(address: str) -> str:
    """
    根据地址获取行政区编码
    Args:
        address: 地址

    Returns:
        行政区编码，如果出错默认返回空
    """
    location = address2location(address)
    if location != '':
        res = location2address(location)
        if res and res.get('status') == 0:
            return str(res.get('result').get('addressComponent').get('adcode'))
    return ''


def weather_search(district_id: str) -> str:
    """

    Args:
        district_id:

    Returns:

    """
    # 接口地址
    url = "https://api.map.baidu.com/weather/v1/"

    params = {
        "district_id": district_id,
        "data_type": "all",
        "ak": os.environ['BAIDU_MAP_API_AK'],
    }

    response = requests.get(url=url, params=params)
    res: dict = response.json() if response else None
    if res is not None:
        if res.get('status') == 0:

            res = res.get('result')
            output = '地点：' + res.get('location').get('country') + res.get('location').get('province') + \
                     res.get('location').get('city') + res.get('location').get('name') + '\n'
            output += '当前天气：' + res.get('now').get('text') + \
                      ' 气温：' + str(res.get('now').get('temp')) + '摄氏度' + \
                      ' 风力：' + res.get('now').get('wind_class') + \
                      ' 风向：' + res.get('now').get('wind_dir') + '\n' + \
                      '明天天气：' + res.get('forecasts')[0].get('text_day') + \
                      ' 气温：' + str(res.get('forecasts')[0].get('low')) + '摄氏度到' + \
                      str(res.get('forecasts')[0].get('high')) + '摄氏度' + \
                      ' 风力：' + res.get('forecasts')[0].get('wc_day') + \
                      ' 风向：' + res.get('forecasts')[0].get('wd_day') + '\n' + \
                      '后天天气：' + res.get('forecasts')[1].get('text_day') + \
                      ' 气温：' + str(res.get('forecasts')[1].get('low')) + '摄氏度到' + \
                      str(res.get('forecasts')[1].get('high')) + '摄氏度' + \
                      ' 风力：' + res.get('forecasts')[1].get('wc_day') + \
                      ' 风向：' + res.get('forecasts')[1].get('wd_day')
            return output
        else:
            return ''
    else:
        return ''
