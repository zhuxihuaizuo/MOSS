# -*- coding: utf-8 -*-
# @Time    : 2023/5/5 下午5:12
# @Author  : Su Yang
# @File    : baidu_map_api.py
# @Software: PyCharm 
# @Comment :
import hashlib
import os
from urllib import parse

import requests


class BaiduMapApi:
    host = 'https://api.map.baidu.com'
    ak = os.environ['BAIDU_MAP_API_AK']
    sk = os.environ['BAIDU_MAP_API_SK']
    use_sn = True if os.environ['BAIDU_MAP_API_SN'] == 'true' else False

    def generate_url(self, uri, params):
        """
        根据设置，生成完整的url
        Args:
            uri: API请求的URI地址，即资源的名称和路径
            params: 请求参数

        Returns:
            完整的请求url
        """
        # 拼接请求字符串
        params_arr = []
        for key in params:
            params_arr.append(key + "=" + str(params[key]))

        query_str = uri + "?" + "&".join(params_arr)

        if self.use_sn:
            # 对queryStr进行转码，safe内的保留字符不转换
            encoded_str = parse.quote(query_str, safe="/:=&?#+!$,;'@()*[]")
            # 在最后直接追加上您的SK
            raw_str = encoded_str + self.sk

            # 计算sn
            sn = hashlib.md5(parse.quote_plus(raw_str).encode("utf8")).hexdigest()

            # 将sn参数添加到请求中
            query_str = query_str + "&sn=" + sn

        # 请注意，此处打印的url为非url encode后的请求串
        # 如果将该请求串直接粘贴到浏览器中发起请求，由于浏览器会自动进行url encode，会导致返回sn校验失败
        url = self.host + query_str
        return url

    def district_place_search(self, query: str, region: str) -> dict:
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
        uri = "/place/v2/search"

        params = {
            "query": query,
            "region": region,
            "page_size": 5,
            "city_limit": 'true',
            "output": "json",
            "scope": 2,
            "ak": self.ak,
        }
        url = self.generate_url(uri, params)
        response = requests.get(url=url)
        res: dict = response.json() if response else None
        return res

    def circle_place_search(self, query: str, user_location: str) -> dict:
        """
        圆形区域检索
        详细信息见: https://lbsyun.baidu.com/faq/api?title=webapi/guide/webservice-placeapi/circle
        Args:
            query: 用户检索需求
            user_location: 区域

        Returns:
            检索结果列表
        """
        uri = "/place/v2/search"

        params = {
            "query": query,
            "location": user_location,
            "page_size": 5,
            "radius": "1500",
            "output": "json",
            "scope": 2,
            "ak": self.ak,
        }
        url = self.generate_url(uri, params)
        response = requests.get(url=url)
        res: dict = response.json() if response else None
        return res

    @staticmethod
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
            return '无法找到有效的搜索结果。'

    def address2location(self, address: str) -> str:
        """
        通过地址获取经纬度
        Args:
            address: 地址

        Returns:
            str：'{lat},{lng}'
        """
        # 接口地址
        uri = "/geocoding/v3"

        params = {
            "address": address,
            "output": "json",
            "ak": self.ak,
        }
        url = self.generate_url(uri, params)
        response = requests.get(url=url)
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

    def location2address(self, location: str) -> dict:
        # 接口地址
        uri = "/reverse_geocoding/v3"

        params = {
            "output": "json",
            "location": location,
            "ak": self.ak,
        }
        url = self.generate_url(uri, params)
        response = requests.get(url=url)
        return response.json() if response else None

    def address2adcode(self, address: str) -> str:
        """
        根据地址获取行政区编码
        Args:
            address: 地址

        Returns:
            行政区编码，如果出错默认返回空
        """
        location = self.address2location(address)
        if location != '':
            res = self.location2address(location)
            if res and res.get('status') == 0:
                return str(res.get('result').get('addressComponent').get('adcode'))
        return ''

    def weather_search(self, district_id: str) -> str:
        """
        天气情况搜索
        Args:
            district_id: 地区的adcode

        Returns:
            天气情况说明
        """
        # 接口地址
        uri = "/weather/v1/"

        params = {
            "district_id": district_id,
            "data_type": "all",
            "ak": self.ak,
        }
        url = self.generate_url(uri, params)
        response = requests.get(url=url)
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
                return '抱歉，无法找到相关天气信息。'
        else:
            return '抱歉，无法找到相关天气信息。'
