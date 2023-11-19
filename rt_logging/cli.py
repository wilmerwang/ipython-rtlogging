import os
import sys
import json
import argparse


def set_args():
    parser = argparse.ArgumentParser(description='Real Time Logging')
    parser.add_argument('--select', '-s', default=-1, type=int, help="Which progress to display?")
    parser.add_argument('--list', '-ls', action="store_true")
    parser.add_argument('--err_flag', '-e', action='store_true', help="Prioritize reading stderr file.")

    args = parser.parse_args()
    return args


CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".ipython-rtlogging.json")


def get_running_path():
    with open(CONFIG_PATH) as f:
        runnings = json.load(f)

    return runnings


def is_file_empty(file_path):
    return os.stat(file_path).st_size == 0


def ls_printer(runnings):
    print("Sort in chronological order of runing code: \n")
    for i, ot in enumerate(runnings.keys()):
        print(i, "  :  ", os.path.dirname(ot), "  ", os.path.basename(ot))


def tail_file(file_path):
    command = f'tail -f {file_path}'
    os.system(command)


def bar_printer(f0, f1):
    if not is_file_empty(f0):
        tail_file(f0)
    elif not is_file_empty(f1):
        tail_file(f1)
    else:
        print("The program progress has not been updated. Please try again later.")


def bar(msg, err_flag):
    path, code = msg
    stdout, stderr = path + '.stdout', path + '.stderr'

    print(code)

    if err_flag:
        bar_printer(stderr, stdout)
    else:
        bar_printer(stdout, stderr)


def main():
    args = set_args()
    select_num = args.select
    ls = args.list
    err_flag = args.err_flag

    runnings = get_running_path()

    if not runnings:
        print("No runing code. Exiting...")
        sys.exit()

    if ls:
        ls_printer(runnings)
    else:
        bar(list(runnings.items())[select_num], err_flag)


if __name__ == "__main__":
    main()