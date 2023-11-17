import os

from IPython.core import magic_arguments
from IPython.core.magic import (
    Magics,
    line_magic,
    cell_magic,
    magics_class,
)

from .tee import StdoutTee, StderrTee


@magics_class
class RealTimeLogMagics(Magics):
    """Magics related to real time logging"""

    def __init__(self, shell):
        super(RealTimeLogMagics, self).__init__(shell)
        # Default execution function used to actually run user code.
        # self.names = set()
        self.names = dict()

    @magic_arguments.magic_arguments()
    @magic_arguments.argument('name', type=str, default='output', nargs='?',
        help="""File Name"""
    )
    @magic_arguments.argument('buffering', type=int, default=-1, nargs='?',
        help="""buffering size, 1 to select line buffering. Same as open(buffering)"""
    )
    @magic_arguments.argument('--no-stderr', action="store_true",
        help="""Don't capture stderr."""
    )
    @magic_arguments.argument('--no-stdout', action="store_true",
        help="""Don't capture stdout."""
    )
    @cell_magic
    def rt_logging(self, line, cell):
        """run the cell, print and redirect stdout, stderr calls."""
        args = magic_arguments.parse_argstring(self.rt_logging, line)
        name = args.name
        buffering = args.buffering

        out = not args.no_stdout
        err = not args.no_stderr

        self.names[name] = cell

        if out and err:
            with StdoutTee(name+".stdout", 'w', buffering), StderrTee(name+".stderr", 'w', buffering):
                self.shell.run_cell(cell)
        elif out and not err:
            with StdoutTee(name+".stdout", 'w', buffering):
                self.shell.run_cell(cell)
        elif not out and err:
            with StderrTee(name+".stderr", 'w', buffering):
                self.shell.run_cell(cell)
        else:
            self.shell.run_cell(cell)

    @magic_arguments.magic_arguments()
    @magic_arguments.argument('--ll', action="store_true",
        help="""File Name to Load"""
    )
    @line_magic
    def ls_logging(self, line, parameter_s=''):
        """list the all logging names"""
        args = magic_arguments.parse_argstring(self.ls_logging, line)
        ll = args.ll
        for name, value in self.names.items():
            if ll:
                print("+" * 10 + " " + name + " " + "+" * 10)
                print(value)
            else:
                print(name)

    @magic_arguments.magic_arguments()
    @magic_arguments.argument('--name', type=str, default=None,
        help="""File Name to Load"""
    )
    @magic_arguments.argument('--top', type=int, default=None,
        help="""top lines to Load"""
    )
    @line_magic
    def load_logging(self, line):
        """load and print logging data"""
        args = magic_arguments.parse_argstring(self.load_logging, line)
        name = args.name
        top = args.top

        if name:
            self._print(name, top)
        else:
            for name, _ in self.names.items():
                self._print(name, top)

    @magic_arguments.magic_arguments()
    @magic_arguments.argument('--name', type=str, default=None,
        help="""File Name to Load"""
    )
    @line_magic
    def rm_logging(self, line):
        """delete logging"""
        args = magic_arguments.parse_argstring(self.load_logging, line)
        name = args.name

        if name:
            self._rm(name)
        else:
            while self.names:
                name = next(iter(self.names))
                self._rm(name)

    def _print(self, name, top=None):
        value = self.names.get(name, None)
        if value:
            header = "+" * 10 + name + " code" + "+" * 10
            print(header)
            print(value)
        files = [name+i for i in ['.stderr', '.stdout']]
        for file in files:
            with open(file, 'r') as f:
                lines = f.readlines()

            if top and top != 0:
                if top > 0:
                    lines = lines[:top]
                else:
                    lines = lines[top:]

            nums = (len(header) - len(file)) // 2
            print("-"*nums + file + "-"*nums)
            print(''.join(lines))

        print('\n\n')

    def _rm(self, name):
        files = [name+i for i in ['.stderr', '.stdout']]
        _ = [os.remove(file) for file in files if os.path.isfile(file)]

        self.names.pop(name, None)


def load_ipython_extension(ipython):
    ipython.register_magics(RealTimeLogMagics)