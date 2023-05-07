# -*- coding: utf-8 -*-
# @Time    : 2023/5/4 下午5:54
# @Author  : Su Yang
# @File    : json2csv_beijing_sight.py
# @Software: PyCharm 
# @Comment :
import csv
import json

with open('../beijing_details_embedding.json', 'r') as f:
    data = json.load(f)

with open('../beijing_details.csv', 'w', newline='') as f:
    writer = csv.writer(f, delimiter=',')
    writer.writerow(['名称', '简介', '地址', '评分', '标签', '内部景点'])

    for sight in data:
        name = sight['name']
        desc = sight['desc'] or ' '
        address = sight['address'] or ' '
        rating = sight['rating'] or 2.5
        tags = sight['tags'] if sight['tags'] != ';' else ' '
        inner_sight = ''
        for sub_sight in sight['subSight']:
            if inner_sight != '':
                inner_sight += ','
            inner_sight += sub_sight['name']
        if inner_sight == '':
            inner_sight = '没有内部景点信息'
        writer.writerow([name, desc, address, rating, tags, inner_sight])
