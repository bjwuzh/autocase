# coding=utf-8
import json
import os
from collections import OrderedDict
from axxac.path_tool import *


# 加载itest中导出的目标json格式的文件
# json_file：传入一个从itest中导出的json文件
def read_itest_json(json_file):
    if not os.path.isfile(json_file):
        return None
    else:
        file_data = open(json_file, encoding='utf-8')
        return json.load(file_data)


def get_header_list(header):
    header_list = []
    for header_item in header:
        header_list.append(
            {
                "name": str(header_item[0]),
                "value": str(header_item[1]),
                "enable": True,
                "encode": True,
                "file": False,
                "required": True,
                "valid": True
            }
        )
    return header_list


def get_assert_list(the_assert):
    assert_list = []
    for assert_item in the_assert:
        assert_list.append(
            {
                "type": "JSON",
                "expression": str(assert_item[0]),
                "expect": str(assert_item[1]),
                "description": str(assert_item[2])
            }
        )
    return assert_list


def get_extract_list(extract):
    extract_list = []
    for extract_item in extract:
        extract_list.append(
            {
                "type": "JSONPath",
                "variable": str(extract_item[0]),
                "value": "${"+str(extract_item[0])+"}",
                "expression": str(extract_item[1]),
                "multipleMatching": False,
                "valid": True
            }
        )
    return extract_list


def generate_header_item(row):
    request_item = OrderedDict([
        ("name", row[0]),
        ("value", row[1]),
        ("enable", True),
        ("encode", True),
        ("file", False),
        ("required", True),
        ("valid", True)
    ])
    return request_item


def generate_login_item(login_config):
    config = login_config['config']
    header = login_config['header']
    a_assert = login_config['assert']
    extract = login_config['extract']

    name = config[0]
    url = config[1]
    username = config[2]
    password = config[3]

    assert_list = get_assert_list(a_assert)
    extract_list = get_extract_list(extract)
    header_list = get_header_list(header)

    raw = {
        "type": 'oa',
        "rememberMe": False,
        "username": username,
        "password": password
    }

    # itest平台原因，需要保持request顺序才能正常解析
    item = OrderedDict([
        ("type", "HTTP"),
        ("name", name),
        ("enable", True),
        ("assertions", {
            "jsonPath": assert_list
        }),
        ("extract", {
            "json": extract_list
        }),
        ("url", url),
        ("method", "POST"),
        ("parameters", [{
            "type": "text",
            "enable": True,
            "contentType": "text/plain",
            "encode": True,
            "file": False,
            "required": True,
            "valid": False
        }]),
        ("headers", header_list),
        ("body", {
            "type": "Raw",
            "raw": json.dumps(raw, indent=4, ensure_ascii=False),
            "kvs": [{
                "type": "text",
                "enable": True,
                "contentType": "text/plain",
                "encode": True,
                "file": False,
                "required": True,
                "valid": False
            }],
            "format": "text",
            "json": False,
            "kV": False,
            "oldKV": False,
            "valid": True,
            "xml": False
        })
    ])
    return item


def generate_request_item(header, row, the_assert):
    raw = dict()
    for i in range(5, len(row)):
        raw[header[i]] = row[i]

    assert_list = get_assert_list(the_assert)

    # itest平台原因，需要保持request顺序才能正常解析
    item = OrderedDict([
        ("type", "HTTP"),
        ("name", row[2]),
        ("enable", True),
        ("assertions", {
            "jsonPath": assert_list
        }),
        ("url", row[1]),
        ("method", "POST"),
        ("parameters", [{
            "type": "text",
            "enable": True,
            "contentType": "text/plain",
            "encode": True,
            "file": False,
            "required": True,
            "valid": False
        }]),
        ("headers", [{
            "enable": True,
            "encode": True,
            "file": False,
            "required": True,
            "valid": False
        }]),
        ("body", {
            "type": "Raw",
            "raw": json.dumps(raw, indent=4, ensure_ascii=False),
            "kvs": [{
                "type": "text",
                "enable": True,
                "contentType": "text/plain",
                "encode": True,
                "file": False,
                "required": True,
                "valid": False
            }],
            "format": "json",
            "json": False,
            "kV": False,
            "oldKV": True,
            "valid": False,
            "xml": False
        })
    ])
    return item


def generate(result_json, login_config, output_dir):
    case_list = result_json['case_list']
    header = result_json['header']
    normal_assert = result_json['normal_assert']
    fail_assert = result_json['fail_assert']

    # 读取itest导出的json文件
    itest_json = read_itest_json(get_cur_dir()+'/itest_template.json')

    # 每一个header
    header_items = []
    for row_num in range(0, len(header)):
        header_item = generate_header_item(header[row_num])
        header_items.append(header_item)
        itest_json['scenarios'][0]['headers'] = header_items

    # 每一条case
    case_items = list()
    if login_config:
        case_items.append(generate_login_item(login_config))

    for row_num in range(1, len(case_list)):
        is_normal = row_num == 1
        the_assert = normal_assert if is_normal else fail_assert
        case_item = generate_request_item(case_list[0], case_list[row_num], the_assert)
        case_items.append(case_item)
        itest_json['scenarios'][0]['requests'] = case_items # itest格式item数组下只取1个元素

    # 写文件
    itest_json_str = json.dumps(itest_json, indent=4, ensure_ascii=False)
    output_dir = get_output_dir(output_dir)
    path = output_dir +'/itest.json'
    with open(path, 'w', encoding='utf-8') as file:
        file.write(itest_json_str)
    print("iTest JSON文件已生成："+os.path.abspath(path))

    return itest_json
