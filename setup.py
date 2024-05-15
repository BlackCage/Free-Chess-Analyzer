import os
import codecs
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

setup(
    name="chess.com-analyzer",
    version="0.2",
    description="Chess.com Analyzer: where you can analyze games endlessly, all without breaking the bank unlike those other guys at Chess.com.",
    long_description_content_type="text/markdown",
    long_description=long_description,
    author="BlackCage",
    author_email="blackcage_faq@proton.me",
    url="https://github.com/BlackCage/Free-Chess-Analyzer",
    packages=find_packages(),
    install_requires=[
        'chessdotcom',
        'requests',
        'websockets',
        'fake_useragent'
    ],
    classifiers=[
        "Topic :: Games/Entertainment :: Board Games",
        "Topic :: Games/Entertainment :: Turn Based Strategy",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13"
    ],
)