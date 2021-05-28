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
                "valid": True,
                "contentType": "",
                "description": ""
            }
        )
    return header_list


def get_extract_list(extract):
    extract_list = []
    for header_item in extract:
        header_item.append(
            {
                "type": "JSONPath",
                "variable": str(header_item[0]),
                "value": str(header_item[1]),
                "expression": "获取"+str(header_item[0])
            }
        )
    return extract_list


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
        ("contentType",""),
        ("description", ""),
        ("enable",True),
        ("encode", True),
        ("file", False),
        ("name", row[0]),
        ("required",True),
        ( "valid", True),
        ("value",  row[1])
    ])
    return request_item


def generate_extract_item(row):
    extract_item = OrderedDict([
        ("type","JSONPath"),
        ("variable",row[0]),
        ("value", row[1]),
        ("expression","获取"+row[0])
    ])
    return extract_item


def generate_extract_item_null():
    extract_item = OrderedDict([
        ("type","JSONPath"),
        ("variable",""),
        ("value", ""),
        ("expression","")
    ])
    return extract_item


def is_json_str(object):
    try:
        json.loads(object)
    except ValueError:
        return False
    return True


def generate_request_item(header, method, title, row, the_assert, extract):
    raw = dict()
    querys_items = []
    for i in range(6, len(row)):
        value = row[i]
        if is_json_str(value):
            value = json.loads(value) # 如果是json字符串，转成json对象
        raw[title[i]] = value

    if method == "POST":
        query_item2 = OrderedDict([
            ("contentType", "text/plain"),
            ("enable", True),
            ("encode", True),
            ("file", False),
            ("required", True),
            ("type", "text"),
            ("valid", False),
            ("name", ""),
            ("value", "")
        ])
        querys_items.append(query_item2)
    else:
        raw = ""
        for i in range(6, len(row)):
            qname = title[i]
            qvalue = row[i]
            query_item1 = OrderedDict([
                ("contentType", "text/plain"),
                ("enable", True),
                ("encode", True),
                ("file", False),
                ("required", True),
                ("type", "text"),
                ("valid", False),
                ("name", qname),
                ("value", qvalue)
            ])
            querys_items.append(query_item1)





    assert_list = get_assert_list(the_assert)
    # 每一个header
    header_items = []
    for row_num in range(0, len(header)):
        header_item = generate_header_item(header[row_num])
        header_items.append(header_item)

    # 每一个提取
    extract_items = []
    for row_num in range(0, len(extract)):
        extract_item = generate_extract_item_null()
        extract_items.append(extract_item)

    item1 = OrderedDict([
        ("name",row[2]),
        ("priority",row[5]),
        ("request",{
        "type": "HTTPSamplerProxy",
        "hashTree": [
            {
                "type": "Assertions",
                "text": [

                ],
                "regex": [

                ],
                "jsonPath": assert_list,
                 "jsr223": [

                      ],
                "xpath2": [

                ],
                "duration": {
                "type": "Duration"
                },
                "enable": True,
                "name": "断言的名字",
                "active": True
            },
            {
                "type": "Extract",
                "regex": [

                ],
                "json": extract_items,
                "xpath": [

                ],
                "enable": True,
                "name": "提取的名字",
                "active": True
            }
        ],
        "customizeReq": False,
        "headers": header_items,
        "body": {
            "raw": json.dumps(raw, indent=4, ensure_ascii=False),
            "type": "JSON",
            "valid": True,
            "xml": False

        },
        "followRedirects": False,
        "doMultipartPost": False,
        "arguments": querys_items
    })
    ])



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
        ("parameters",method ),
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
    return item1


def generate(result_json, output_dir):
    method = result_json['method']
    header = result_json['header']
    case_list = result_json['case_list']
    normal_assert = result_json['normal_assert']
    fail_assert = result_json['fail_assert']
    extract = result_json['extract']
    # 读取itest导出的json文件
    itest_json = read_itest_json(get_cur_dir()+'/itest_template.json')



    # 每一条case
    case_items = list()

    for row_num in range(1, len(case_list)):
        is_normal = row_num == 1
        the_assert = normal_assert if is_normal else fail_assert
        case_item = generate_request_item(header, method, case_list[0], case_list[row_num], the_assert, extract)
        case_items.append(case_item)
        itest_json = case_items # itest格式item数组下只取1个元素

    # 写文件
    itest_json_str = json.dumps(itest_json, indent=4, ensure_ascii=False)
    output_dir = get_output_dir(output_dir)
    path = output_dir +'/itest.json'
    with open(path, 'w', encoding='utf-8') as file:
        file.write(itest_json_str)
    print("iTest JSON文件已生成："+os.path.abspath(path))

    return itest_json
