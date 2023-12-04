from setuptools import setup, find_packages

setup(
    name='done',
    version='0.0.0',
    packages=find_packages(),
    extras_require={
        'test': ['pytest']
    }
)
