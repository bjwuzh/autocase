from axxac import read_require_config
import json
from collections import OrderedDict


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

def generate_request_item(name, url, method, query, header, body, the_assert, extract):
    query_list = get_query_list(query)

    raw = dict()
    for row_num in range(len(body)):
        body_row = body[row_num]
        raw[body_row[0]] = body_row[1]

    header_list = get_header_list(header)
    assert_list = get_assert_list(the_assert)
    extract_list = get_extract_list(extract)


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
        ("method", method),
        ("parameters", query_list),
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
            "format": "json",
            "json": False,
            "kV": False,
            "oldKV": True,
            "valid": False,
            "xml": False
        })
    ])
    return item

def generate_require_items(requires_dir):
    require_items =[]
    result_json_array = read_require_config.read_excel(requires_dir)
    for row_num in range(0, len(result_json_array)):
        result_json = result_json_array[row_num]
        name = result_json['name']
        url = result_json['url']
        method = result_json['method']
        query = result_json['query']
        header = result_json['header']
        body = result_json['body']
        the_assert = result_json['normal_assert']
        extract = result_json['extract']

        require_item = generate_request_item(name, url, method, query, header, body, the_assert, extract)
        require_items.append(require_item)

    return require_items