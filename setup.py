from setuptools import setup, find_packages

setup(
    name='sync_folders',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'pytest',
        'setuptools',
        'xxhash'],
)
