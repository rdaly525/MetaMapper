from setuptools import setup
import sys

setup(
    name='metamapper',
    version='0.0.1',
    url='https://github.com/rdaly525/MetaMapper',
    license='MIT',
    maintainer='Ross Daly',
    maintainer_email='rdaly525@stanford.edu',
    description='A Mapper constructor for CoreIR',
    packages=[
        "metamapper"
    ],
    install_requires=[
        "coreir >= 2.0.1",
        "peak",
        "DagVisitor",
        "delegator.py"
    ],
    python_requires='>=3.6'
)
