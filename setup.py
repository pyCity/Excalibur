from setuptools import setup, find_packages

setup(
    name='src',
    version='0.1dev',
    packages=find_packages(),
    url='https://github.com/pyCity/src',
    license=open("LICENSE", "r").read(),
    author='pyCity',
    author_email='',
    description=open("README.md", "r").read(),
    py_modules=[
        'src/classes',
        'src/functions',
        'src/variables'
    ],
    install_requires=[
        "pycryptodome >= 3.8.1",
        "tqdm >= 4.31.1"
    ],
)

