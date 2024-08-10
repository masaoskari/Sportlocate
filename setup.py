"""Basic setup py file for installing and packaging Sportlocate."""
from setuptools import setup, find_packages


setup(
    name='sportlocate',
    version='1.0.0',
    author='Pythonic',
    description='Description of your package',
    packages=find_packages(),
    install_requires=["requests", "pandas", "dataclasses", "folium", "pyqt5", "PyQtWebEngine", "geopy", "retry"],
    entry_points={"console_scripts": ["sportlocate=src.sportlocate.__main__:main"]},
    include_package_data=True,
)