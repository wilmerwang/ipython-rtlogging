"""
This is copied and modified based on the tee (https://github.com/algrebe/python-tee/blob/master/tee/tee.py).
"""
import os
import sys
from abc import abstractmethod


class Tee(object):
    """
    duplicates streams to a file.
    """

    def __init__(self, filename, mode="w", buff=-1):
        """
        writes both to stream and to file.
        both stream must return a string or None.
        """
        self.filename = filename
        self.mode = mode
        self.buff = buff

        self.stream = None
        self.fp = None

    @abstractmethod
    def set_stream(self, stream):
        """
        assigns "stream" to some global variable e.g. sys.stdout
        """
        pass

    @abstractmethod
    def get_stream(self):
        """
        returns the original stream e.g. sys.stdout
        """
        pass

    def write(self, message):
        if message is not None:
            self.stream.write(message)
            self.fp.write(message)

    def flush(self):
        self.stream.flush()
        self.fp.flush()
        os.fsync(self.fp.fileno())

    def __enter__(self):
        self.stream = self.get_stream()
        self.fp = open(self.filename, self.mode, self.buff)
        self.set_stream(self)

    def __exit__(self, *args):
        self.close()

    def close(self):
        if self.stream is not None:
            self.set_stream(self.stream)
            self.stream = None

        if self.fp is not None:
            self.fp.close()
            self.fp = None


class StdoutTee(Tee):
    def set_stream(self, stream):
        sys.stdout = stream

    def get_stream(self):
        return sys.stdout


class StderrTee(Tee):
    def set_stream(self, stream):
        sys.stderr = stream

    def get_stream(self):
        return sys.stderr


if __name__ == "__main__":
    with StdoutTee("mystdout.txt"), StderrTee("mystderr.txt"):
        sys.stdout.write("[stdout] hello\n")
        sys.stderr.write("[stderr] hello\n")
        sys.stdout.write("[stdout] world\n")
        sys.stderr.write("[stderr] world\n")

    sys.stdout.write("[stdout] not going to be written to file\n")
    sys.stderr.write("[stderr] not going to be written to file\n")