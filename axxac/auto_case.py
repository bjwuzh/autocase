# coding=utf-8
from axxac.generate_case_list import generate as clg
from axxac.generate_itest_json import generate as ijg
from axxac.read_login_config import read_excel


def execute(case_config_file, login_config_file, output_dir):
    case_list = clg(case_config_file, output_dir)
    login_config = read_excel(login_config_file)
    ijg(case_list, login_config, output_dir)