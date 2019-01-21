import io

from setuptools import find_packages, setup

with io.open('README.rst', 'rt', encoding='utf8') as f:
    readme = f.read()

setup(
    name='simplecron',
    version='1.0.0',
    maintainer='weidong.huang',
    maintainer_email='weidong.huang@kaixiangtech.com',
    description='basic httpserver for neucli3 task',
    long_description=readme,
    packages = find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'requests',
    ],
)
