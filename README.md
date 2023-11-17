# ipython-rtlogging
## Ipython Real Time Logging
`ipython-rtlogging` is a tool that relies only on the Python standard library (except for IPython) and is used to capture and log the output streams of cells in real-time within IPython or IPython Notebook. It provides an optional solution to tackle the problem of losing cell outputs or not being able to monitor the progress of a running code after reconnecting to the Notebook.

https://github.com/wilmerwang/ipython-rtlogging/assets/35020700/c3e99487-295a-4572-b0ba-f88e90696333



## Dependencies
- ipython

## Install
Install the latest release with:
```bash
pip install ipython-rtlogging
```

or download from [https://github.com/wilmerwang/ipython-rtlogging](https://github.com/wilmerwang/ipython-rtlogging) and:
```bash
cd ipython-rtlogging
python3 setup.py install
```
## Examples
Please cheack [this notebook](doc/doc.ipynb)

## Usage
Load rt_logging in IPython or IPython Notebook: 
```bash
In [1]: %load_ext rt_logging
```

---

There are some extesion magic method:
```bash
In [2]: %%rt_logging?

Docstring:
::

    %rt_logging [--no-stderr] [--no-stdout] [name] [buffering]

run the cell, print and redirect stdout, stderr calls.

positional arguments:
  name         File Name
  buffering    buffering size, 1 to select line buffering. Same as
               open(buffering)

optional arguments:
  --no-stderr  Don't capture stderr.
  --no-stdout  Don't capture stdout.
```

---

```bash
In [3]: %ls_logging?
Docstring:
::

    %ls_logging [--ll]

list the all logging names

optional arguments:
  --ll  File Name to Load
```
---

```bash
In [4]: %load_logging?
Docstring:
::

  %load_logging [--name NAME] [--top TOP]

load and print logging data

optional arguments:
  --name NAME  File Names to Load
  --top TOP    top lines to Load
```

---

```bash
In [5]: %rm_logging?
Docstring:
::

  %rm_logging [--name NAME]

delete logging

optional arguments:
  --name NAME  File Name to Load
```

## License
MIT
