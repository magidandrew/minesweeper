from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='minesweeper',
    version='1.0',
    description='WindowsXP Minesweeper Recreation.',
    author='magidandrew',
    author_email='hq@andrewmagid.com',
    packages=['minesweeper'],
    install_requires=required
)
