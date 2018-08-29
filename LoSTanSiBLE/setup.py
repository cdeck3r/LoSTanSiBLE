from setuptools import find_packages, setup

#
# you may want to read
# https://packaging.python.org/discussions/install-requires-vs-requirements/
# https://caremad.io/posts/2013/07/setup-vs-requirement/
#

setup(
    name='src',
    packages=find_packages(),
    version='0.1.0',
    install_requires=[
        "pandas",
        "numpy",
        "stockstats"
    ],
    description='Low Speed Trading and Small in Budget; Large Expenses - A data science exercise project for stock market trading. ',
    author='Christian Decker',
    license='MIT',
)
