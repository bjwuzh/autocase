# coding=utf-8
import json
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


def get_query_list(query):
    query_list = []
    for query_item in query:
        query_list.append(
            {
                "name": str(query_item[0]),
                "value": str(query_item[1]),
                "type": "text",
                "enable": True,
                "contentType": "text/plain",
                "encode": True,
                "file": False,
                "required": True,
                "valid": True
            }
        )
    return query_list


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


def is_json_str(object):
    try:
        json.loads(object)
    except ValueError:
        return False
    return True


def generate_request_item(method, query, title, row, the_assert):
    query_list = get_query_list(query)

    raw = dict()
    for i in range(5, len(row)):
        value = row[i]
       # if is_json_str(value):
            # value = json.loads(value) # 如果是json字符串，转成json对象
        raw[title[i]] = value

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
        ("method", method),
        ("parameters", query_list),
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


def generate(result_json, require_items, output_dir):
    method = result_json['method']
    query = result_json['query']
    header = result_json['header']
    case_list = result_json['case_list']
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
    if require_items:
        case_items.extend(require_items)

    for row_num in range(1, len(case_list)):
        is_normal = row_num == 1
        the_assert = normal_assert if is_normal else fail_assert
        case_item = generate_request_item(method, query, case_list[0], case_list[row_num], the_assert)
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
