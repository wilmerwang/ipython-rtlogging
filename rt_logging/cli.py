import os
import sys
import json
import argparse
from functools import partial
from threading import Thread, Event

from rich import print
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
from rich.box import ASCII

from .tail import Tail


CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".ipython-rtlogging.json")
OUT = [''] * 10
ERR = [''] * 10


def set_args():
    parser = argparse.ArgumentParser(description='Real Time Logging')
    parser.add_argument('--list', '-ls', action="store_true")

    args = parser.parse_args()
    return args


def get_running_path():
    with open(CONFIG_PATH) as f:
        runnings = json.load(f)

    return runnings


def is_file_empty(file_path):
    return os.stat(file_path).st_size == 0


def ls_printer(runnings):
    table = Table(expand=True, show_edge=False, box=ASCII)
    # table.title = "[red]Sort in chronological order of runing code"
    table.add_column("Index")
    table.add_column("Path")
    table.add_column("Output Name")
    table.add_column("Code")
    table.add_column("Start Date")
    for i, ot in enumerate(runnings.keys()):
        code = Syntax(runnings[ot]['code'], "python", line_numbers=True)
        table.add_row(f'[green]{i}',
                      os.path.dirname(ot),
                      os.path.basename(ot),
                      code,
                      runnings[ot]['start_date'])
    print(table)


def generate_table() -> Table:
    """Make a new table."""
    table = Table(expand=True, show_edge=False, box=ASCII)
    table.add_column("STDOUT")
    table.add_column("STDERR")

    for i in range(len(OUT)):
        table.add_row(
            f"{OUT[i]}", f"{ERR[i]}"
        )
    return table


def auto_put(q, i):
    q = q[-9:]
    q.append(i)
    return q


def update_panel(file_path, txt, live):
    global OUT, ERR
    txt = txt.rstrip('\n')
    if txt != '':
        if file_path.endswith('stdout'):
            OUT = auto_put(OUT, txt)
        else:
            ERR = auto_put(ERR, txt)

        live.update(Panel(generate_table(), title="[red]Output"))


def worker(path, live, done):
    tail = Tail(path)
    func = partial(update_panel, live=live)
    tail.register_callback(func)
    tail.follow(done, s=1)


def output_printer(stdout, stderr):
    done = Event()
    with Live(generate_table(), refresh_per_second=4) as live:
        worker1 = Thread(target=worker, args=(stdout, live, done))
        worker2 = Thread(target=worker, args=(stderr, live, done))
        worker1.start()
        worker2.start()

        try:
            while True:
                pass
        except KeyboardInterrupt:
            # cancel workers
            done.set()

        worker1.join()
        worker2.join()


def bar(msg):
    path, content = msg
    code = content['code']
    stdout, stderr = path + '.stdout', path + '.stderr'

    code = Syntax(code, "python", theme="monokai", line_numbers=True)
    print(Panel(code, title="[red]Code"))

    if is_file_empty(stdout) and is_file_empty(stdout):
        print("The program progress has not been updated. Please try again later.")
        sys.exit()

    output_printer(stdout, stderr)


def main():
    args = set_args()
    ls = args.list

    runnings = get_running_path()

    if not runnings:
        print("No runing code. Exiting...")
        sys.exit()

    if ls:
        ls_printer(runnings)
    else:
        ls_printer(runnings)
        while True:
            try:
                select_str = input("Select Index (None means -1): ")
                if select_str == '':
                    select_num = -1
                else:
                    select_num = int(select_str)

                if -len(runnings) <= select_num < len(runnings):
                    break
            except ValueError:
                pass
            print("Invalid input. Please enter a valid index.")

        bar(list(runnings.items())[select_num])


if __name__ == "__main__":
    main()