# coding=utf-8
import sys
import getopt
from axxac.auto_case import execute

HELP = 'Usage:\n  axxac -c <case_config_file> -l <login_config_file> -o <output_directory>'


def run(argv, help_info):
    argv = argv[1:]
    if len(argv) == 0:
        print(help_info)
        sys.exit()
    case_config_file = ''
    login_config_file = ''
    output_dir = ''
    try:
        opts, args = getopt.getopt(argv, "hc:l:o:")
    except getopt.GetoptError:
        print(help_info)
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print(help_info)
            sys.exit()
        elif opt == "-c":
            case_config_file = arg
        elif opt == "-l":
            login_config_file = arg
        elif opt == "-o":
            output_dir = arg

    execute(case_config_file, login_config_file, output_dir)


if __name__ == '__main__':
    run(sys.argv, HELP)


def cmdexe():
    run(sys.argv, HELP)