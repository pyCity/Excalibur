from setuptools import setup, find_packages

setup(
    name='src',
    version='0.1dev',
    packages=find_packages(),
    url='https://github.com/pyCity/Excalibur',
    author='pyCity',
    license=open("LICENSE", "r").read(),
    description=open("README.md", "r").read(),
    install_requires=open("requirements.txt", "r").read(),
    py_modules=[
        'src/classes',
        'src/functions',
        'src/variables',
        'src/main',
        "src/__init__.py"
    ],
)
