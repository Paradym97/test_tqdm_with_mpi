from setuptools import setup, find_packages

setup(
    name='tqdm_mpi',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        'tqdm',
        'mpi4py',
    ],
)