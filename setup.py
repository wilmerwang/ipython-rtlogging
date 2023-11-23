import os
from setuptools import find_packages, setup


here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, "README.md"), encoding="utf-8").read()


version = "0.2.3"

install_requires = [
    "ipython>=8.0",
    "rich>=13.0"
]

setup(
    name="ipython-rtlogging",
    version=version,
    author="wilmerwang",
    author_email="280458666@qq.com",
    description="real time logging via IPython",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/wilmerwang/ipython-rtlogging",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "rt_logging = rt_logging.cli:main",
        ]
    },
    keywords="logging ipython real-time reconnection",
    packages=find_packages(),
    install_requires=install_requires
)
