# coding=utf-8
import xlrd


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


def read_excel(excel_file):
    if not excel_file:
        return None

    data = xlrd.open_workbook(excel_file)
    config_sheet = data.sheet_by_index(0)
    header_sheet = data.sheet_by_index(1)
    assert_sheet = data.sheet_by_index(2)
    extract_sheet = data.sheet_by_index(3)

    login_result_json = dict()
    login_result_json["config"] = get_config_value(config_sheet)
    login_result_json["header"] = get_header_value(header_sheet)
    login_result_json["assert"] = get_assert_value(assert_sheet)
    login_result_json["extract"] = get_token_value(extract_sheet)
    return login_result_json
