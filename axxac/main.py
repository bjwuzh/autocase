# coding=utf-8
import sys
import getopt
from axxac.auto_case import execute

HELP = 'Usage:\n  axxac -i <input_directory> -o <output_directory>'


def run(argv, help_info):
    argv = argv[1:]
    if len(argv) == 0:
        print(help_info)
        sys.exit()
    input_dir = ''
    output_dir = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:")
    except getopt.GetoptError:
        print(help_info)
        sys.exit()
    for opt, arg in opts:
        if opt == '-h':
            print(help_info)
            sys.exit()
        elif opt == "-i":
            input_dir = arg
        elif opt == "-o":
            output_dir = arg

    execute(input_dir, output_dir)


if __name__ == '__main__':
    execute("../data", "../output/")
    # run(sys.argv, HELP)

def cmdexe():
    run(sys.argv, HELP)