# coding=utf-8
from axxac.generate_case_list import generate as clg
from axxac.generate_itest_json import generate as ijg
from axxac.require import generate_require_items
from axxac.path_tool import get_cases_dir, get_requires_dir

def execute(input_dir, output_dir):
    case_result_json = clg(get_cases_dir(input_dir), output_dir)
    require_items = generate_require_items(get_requires_dir(input_dir))
    ijg(case_result_json, require_items, output_dir)