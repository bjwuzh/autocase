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