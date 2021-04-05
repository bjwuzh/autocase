# coding=utf-8
import xlrd
import os


def get_name(sheet):
    return sheet.row_values(1)[0]


def get_url(sheet):
    return sheet.row_values(1)[1]


def get_method(sheet):
    return sheet.row_values(1)[2]


def get_query(sheet):
    query_rows = []
    for row_num in range(1, sheet.nrows):
        row_values = sheet.row_values(row_num)
        query_rows.append(row_values)
    return query_rows


def get_header(sheet):
    header_rows = []
    for row_num in range(1, sheet.nrows):
        row_values = sheet.row_values(row_num)
        header_rows.append(row_values)
    return header_rows


def get_body(sheet):
    body_rows = []
    for row_num in range(1, sheet.nrows):
        row_values = sheet.row_values(row_num)
        body_rows.append(row_values)
    return body_rows

def remove_tail_space(array):
    new_array = array[:]
    for i in range(len(new_array)-1, -1, -1):
        if new_array[i] == '':
            array.pop()
        else:
            break


def get_assert(sheet):
    assert_rows = []
    for row_num in range(1, sheet.nrows):
        row_values = sheet.row_values(row_num)
        assert_rows.append(row_values)
    return assert_rows

def get_extract(sheet):
    extract_rows = []
    for row_num in range(1, sheet.nrows):
        row_values = sheet.row_values(row_num)
        extract_rows.append(row_values)
    return extract_rows

def get_config_value(sheet):
    row_values = sheet.row_values(1)
    return row_values


def get_header_value(sheet):
    header_rows = []
    for row_num in range(1, sheet.nrows):
        row_values = sheet.row_values(row_num)
        header_rows.append(row_values)
    return header_rows


def get_token_value(sheet):
    token_rows = []
    for row_num in range(1, sheet.nrows):
        row_values = sheet.row_values(row_num)
        token_rows.append(row_values)
    return token_rows


def get_assert_value(sheet):
    assert_rows = []
    for row_num in range(1, sheet.nrows):
        row_values = sheet.row_values(row_num)
        assert_rows.append(row_values)
    return assert_rows


def read_excel(requires_dir):
    if not os.path.isdir(requires_dir):
        return None

    result_json_array = []
    items = os.listdir(requires_dir)
    items.sort(key=lambda x: int(x.split('-')[0])) # 升序排序
    for item in items:
        path = os.path.join(requires_dir, item)
        if os.path.isfile(path):
            data = xlrd.open_workbook(path)
            cfg_sheet = data.sheet_by_index(0)
            query_sheet = data.sheet_by_index(1)
            header_sheet = data.sheet_by_index(2)
            body_sheet = data.sheet_by_index(3)
            assert_normal_sheet = data.sheet_by_index(4)
            assert_fail_sheet = data.sheet_by_index(5)
            extract_sheet = data.sheet_by_index(6)

            result_json = dict()
            result_json["name"] = get_name(cfg_sheet)
            result_json["url"] = get_url(cfg_sheet)
            result_json["method"] = get_method(cfg_sheet)
            result_json["query"] = get_query(query_sheet)
            result_json["header"] = get_header(header_sheet)
            result_json["body"] = get_body(body_sheet)
            result_json["normal_assert"] = get_assert(assert_normal_sheet)
            result_json["fail_assert"] = get_assert(assert_fail_sheet)
            result_json["extract"] = get_extract(extract_sheet)

            result_json_array.append(result_json)

    return result_json_array
