# coding=utf-8
import xlrd


def get_first_unit_value(sheet):
    return sheet.row_values(0)[0]


def get_header(sheet):
    header_rows = []
    for row_num in range(1, sheet.nrows):
        row_values = sheet.row_values(row_num)
        header_rows.append(row_values)
    return header_rows


def get_params(sheet):
    params = []
    for col_num in range(sheet.ncols):
        col_values = sheet.col_values(col_num)
        remove_tail_space(col_values) # 删除每列最后由于列值个数不同而自动生成的空字符串
        param = dict()
        param['name'] = col_values[0]
        param['values'] = col_values[1:]
        params.append(param)
    return params


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


def read_excel(excel_file):
    data = xlrd.open_workbook(excel_file)
    name_sheet = data.sheet_by_index(0)
    url_sheet = data.sheet_by_index(1)
    header_sheet = data.sheet_by_index(2)
    params_sheet = data.sheet_by_index(3)
    assert_normal_sheet = data.sheet_by_index(4)
    assert_fail_sheet = data.sheet_by_index(5)

    result_json = dict()
    result_json["name"] = get_first_unit_value(name_sheet)
    result_json["url"] = get_first_unit_value(url_sheet)
    result_json["header"] = get_header(header_sheet)
    result_json["params"] = get_params(params_sheet)
    result_json["normal_assert"] = get_assert(assert_normal_sheet)
    result_json["fail_assert"] = get_assert(assert_fail_sheet)
    return result_json
