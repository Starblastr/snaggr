# setup.py
from setuptools import setup, find_packages

setup(
    name='snaggr',
    version='0.12',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scikit-learn',
        'selenium',
        'beautifulsoup4',
        'pandas'
    ],
    description='A package for scraping hotel reviews from google, which uses selenium as its backbone.',
    author='Deon Posey',
    author_email='deonposey@gmail.com',
    url='https://github.com/Starblastr/snaggr',
        classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)