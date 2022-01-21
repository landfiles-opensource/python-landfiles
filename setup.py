from setuptools import setup, find_packages


setup(
    name="landfiles",
    version="0.0.1",
    url="https://github.com/Vayel/python-landfiles",
    packages=find_packages(),
    include_package_data=True,
    install_requires=["requests",],
)
