# coding=utf-8
from axxac import read_case_config
import time
import xlwt
from axxac.path_tool import *
import os


def write_excel_xls(path, sheet_name, value):
    index = len(value)
    workbook = xlwt.Workbook()
    worksheet = workbook.add_sheet(sheet_name)
    for i in range(0, index):
        for j in range(0, len(value[i])):
            worksheet.write(i,j, str(value[i][j]))
    workbook.save(path)


def get_normal_values(params):
    normal_values = []
    for param in params:
        values = param['values']
        normal_values.append(values[0])
    return normal_values

def get_src_file(case_dir):
    # 目前只支持第一个文件
    items = os.listdir(case_dir)
    for item in items:
        path = os.path.join(case_dir, item)
        if os.path.isfile(path):
            return path
    return ''

def generate(cases_dir, output_dir):
    origin_header = ['接口名称', '接口', '测试场景', '是否完成', '编写完成日期','优先级']
    header = []
    header.extend(origin_header)
    case_list = [header]
    src_json = read_case_config.read_excel(get_src_file(cases_dir))
    api_name = src_json['name']
    url = src_json['url']
    method = src_json['method']
    body = src_json['body']
    request_header = src_json['header']
    normal_assert = src_json['normal_assert']
    fail_assert = src_json['fail_assert']
    extract = src_json['extract']

    normal_values = get_normal_values(body)
    param_parts = [['所有参数都正确','P0', normal_values]]  # 第一个元素为场景名

    for i in range(len(body)):
        param = body[i]
        name = param['name']
        header.append(name)

        values = param['values']
        # 遍历异常值，从第2个开始，第1个为正确值
        for j in range(1, len(values)):
            error_value = values[j]
            error_values = []
            error_values.extend(normal_values)
            error_values[i] = error_value
            param_parts.append([str(name)+'='+str(error_value), 'P2', error_values])  # 第一个元素为场景名

    for i in range(len(param_parts)):
        param = param_parts[i]
        row = list()
        row.append(api_name)
        row.append(url)
        row.append(param[0])  # 场景名
        row.append('true')
        row.append(time.strftime('%Y-%m-%d', time.localtime()))
        row.append(param[1])
        row.extend(param[2])
        case_list.append(row)

    # 写excel
    output_dir = get_output_dir(output_dir)
    path = output_dir+'/case_list.xls'
    write_excel_xls(path, 'sheet1', case_list)
    print("\n测试用例表格已生成："+os.path.abspath(path)+"\n")

    # 加上请求方法、请求头、断言信息，用于itest json生成
    result_json = {
        "case_list": case_list,
        "method": method,
        "header": request_header,
        "normal_assert": normal_assert,
        "fail_assert": fail_assert,
        "extract": extract
    }
    return result_json

