import subprocess
from setuptools import setup

with open('requirements/run.txt') as f:
    requirements = [line for line in f]

version = subprocess.check_output(
    'git rev-list HEAD --count',
    shell=True).strip().decode('utf-8')

setup(
    name='pypl',
    version=version,
    install_requires=requirements,
    author='Ingo Fruend',
    author_email='pypl@ingofruend.net',
    packages=['pypl'],
)
