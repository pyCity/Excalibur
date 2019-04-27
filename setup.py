from setuptools import setup, find_packages

setup(
    name='Excalibur',
    version='0.1.dev',
    packages=find_packages(),
    url='https://github.com/pyCity/Excalibur',
    author='pyCity',
    license=open("LICENSE", "r").read(),
    description=open("README.md", "r").read(),
    install_requires=open("requirements.txt", "r").read(),
)
