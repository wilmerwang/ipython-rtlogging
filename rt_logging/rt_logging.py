import os
import json
import datetime

from IPython.core import magic_arguments
from IPython.core.magic import (
    Magics,
    line_magic,
    cell_magic,
    magics_class,
)
from IPython.display import display, HTML, Code

from .tee import StdoutTee, StderrTee


@magics_class
class RealTimeLogMagics(Magics):
    """Magics related to real time logging"""

    def __init__(self, shell):
        super(RealTimeLogMagics, self).__init__(shell)
        # Default execution function used to actually run user code.
        # self.names = set()
        self.names = dict()

        self.home = os.path.expanduser("~")
        self.config_path = os.path.join(self.home, ".ipython-rtlogging.json")
        self.log_dir = os.getcwd()
        self._prepare()

    def _prepare(self):
        try:
            with open(self.config_path, 'r') as f:
                self.configs = json.load(f)
        except:
            self.configs = {}

    @magic_arguments.magic_arguments()
    @magic_arguments.argument('name', type=str, default='output',
        help="""File Name"""
    )
    @magic_arguments.argument('--buffering', type=int, default=1,
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

        # log the runing cell 
        current_time = datetime.datetime.now()
        current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
        self.configs.setdefault(os.path.join(self.log_dir, name), {})['code'] = cell
        self.configs[os.path.join(self.log_dir, name)]['start_date'] = current_time_str

        self._save_config()

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
            self.configs.pop(os.path.join(self.log_dir, name))
            self._save_config()
            self.shell.run_cell(cell)

        self.configs.pop(os.path.join(self.log_dir, name))
        self._save_config()

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
                header = "+" * 10 + " " + name + " " + "+" * 10
                display(HTML('<h4 style="color: red;">{}</h4>'.format(header)))
                display(Code(value))
            else:
                display(name)

    @magic_arguments.magic_arguments()
    @magic_arguments.argument('--name', type=str, default=None, nargs='+',
        help="""File Names to Load"""
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
            if isinstance(name, list):
                for n in name:
                    self._print(n, top)
            else:
                self._print(name, top)
        else:
            for name, _ in self.names.items():
                self._print(name, top)

    @magic_arguments.magic_arguments()
    @magic_arguments.argument('--name', type=str, default=None, nargs="+",
        help="""File Name to Load"""
    )
    @line_magic
    def rm_logging(self, line):
        """delete logging"""
        args = magic_arguments.parse_argstring(self.load_logging, line)
        name = args.name

        if name:
            if isinstance(name, list):
                for n in name:
                    self._rm(n)
            else:
                self._rm(name)
        else:
            while self.names:
                name = next(iter(self.names))
                self._rm(name)

    def _print(self, name, top=None):
        value = self.names.get(name, None)
        if value:
            header = "+" * 10 + " " + name + " " + " code " + "+" * 10
            display(HTML('<h4 style="color: red;">{}</h4>'.format(header)))
            display(Code(value))

        files = [name+i for i in ['.stderr', '.stdout']]
        for file in files:
            if os.path.isfile(file):
                with open(file, 'r') as f:
                    lines = f.readlines()
                if len(lines) > 0:
                    if top and top != 0:
                        if top > 0:
                            lines = lines[:top]
                        else:
                            lines = lines[top:]

                    header2 = "="*12 + " " + file + " " + "="*12
                    display(HTML('<h5 style="color: green;">{}</h5>'.format(header2)))
                    print(''.join(lines))

    def _rm(self, name):
        files = [name+i for i in ['.stderr', '.stdout']]
        _ = [os.remove(file) for file in files if os.path.isfile(file)]

        self.names.pop(name, None)

    def _save_config(self):
        with open(self.config_path, 'w') as f:
            json.dump(self.configs, f)


def load_ipython_extension(ipython):
    ipython.register_magics(RealTimeLogMagics)