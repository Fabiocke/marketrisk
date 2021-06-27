
from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()


setup(name='marketrisk',
    version='0.0.3',
    license='MIT License',
    author='Fábio Minutti Teixeira',
    long_description=readme,
    author_email='fabiomt92@hotmail.com',
    keywords=['risco', 'mercado', 'var', 'value at risk', 'market', 'risk'],
    description='Classes para calculos de risco de mercado',
    packages=['marketrisk'],
    install_requires=['numpy', 'pandas_datareader'])

        