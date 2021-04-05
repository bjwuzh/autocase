# coding=utf-8
import os


def get_cur_dir():
    return os.path.dirname(__file__)


def get_output_dir(output_dir):
    if not output_dir or os.path.isfile(output_dir):
        output_dir = '.'
    elif not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return output_dir


def get_cases_dir(input_dir):
    if os.path.isdir(input_dir):
        return os.path.join(input_dir, 'cases')
    return ''

def get_requires_dir(input_dir):
    if os.path.isdir(input_dir):
        return os.path.join(input_dir, 'requires')
    return ''