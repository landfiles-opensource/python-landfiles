from landfile import __version__
from setuptools import setup, find_packages


setup(
    name="landfiles",
    version=__version__,
    url="https://github.com/Vayel/python-landfiles",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["requests",],
)
