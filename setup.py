# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='CodeDependencyVisualizer',
    version='0.1.0',
    description='Code Dependency Visualizer',
    long_description=readme,
    author='Ahmed Abdel Aal',
    author_email='eng.ahmedhussein89@gmail.com',
    url='https://github.com/wow2006/CodeDependencyVisualizer',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

