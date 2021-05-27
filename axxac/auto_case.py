# coding=utf-8
from axxac.generate_case_list import generate as clg
from axxac.generate_itest_json import generate as ijg
from axxac.require import generate_require_items

def execute(input_dir, output_dir):
    case_result_json = clg(input_dir, output_dir)
    ijg(case_result_json, output_dir)