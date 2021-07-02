# coding=utf-8
import axxac.generate_case_list as clg
import  axxac.generate_itest_json as ijg


def execute(input_dir, output_dir):
    case_result_json = clg.GenerateCase.generate(input_dir)
    ijg.Generatejson.generate(case_result_json, output_dir)