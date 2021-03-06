# https://python-packaging.readthedocs.io/en/latest/minimal.html
# https://marthall.github.io/blog/how-to-package-a-python-app/
# https://github.com/pypa/sampleproject
# https://stackoverflow.com/a/20234833
# https://mike.zwobble.org/2013/05/adding-git-or-hg-or-svn-dependencies-in-setup-py/
# https://setuptools.readthedocs.io/en/latest/setuptools.html#using-find-packages
# https://danielsokolowski.blogspot.de/2012/08/setuptools-includepackagedata-option.html

from setuptools import setup, find_packages

setup(
    name='pyd3ckservice',
    version='0.0.1',
    description='Test project, do not use in production!',
    include_package_data=True,  # enable MANIFEST.in
    packages=find_packages(exclude=['examples']),
    install_requires=['pyd3ckbase>=0.0.1'],
    dependency_links=[
        'git+https://github.com/d3ck-org/pyd3ckbase.git#egg=pyd3ckbase-0.0.1'
    ])
