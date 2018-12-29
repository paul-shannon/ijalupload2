import io
import os
import re

from setuptools import find_packages
from setuptools import setup


def read(filename):
    filename = os.path.join(os.path.dirname(__file__), filename)
    text_type = type(u"")
    with io.open(filename, mode="r", encoding='utf-8') as fd:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), fd.read())


setup(
    name="ijaltexts",
    version="0.1.0",
    url="https://github.com/paul-shannon/ijaltexts",
    license='MIT',

    author="Paul Shannon",
    author_email="paul.thurmond.shannon@gmail.com",

    description="Transform markup and sound into an interlinear webpage",
    long_description=read("README.rst"),

    packages=find_packages(exclude=('tests',)),

    install_requires=['xmlschema',
                      'scipy',
                      'dash',
                      'pandas',
                      'dash_table',
                      'pyyaml',
                      'dash_core_components',
                      'dash_html_components',
                      ],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
