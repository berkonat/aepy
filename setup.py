import os
import re
import sys
import glob
import sysconfig
import platform
import subprocess

from distutils.version import LooseVersion

try:
    from setuptools import setup, Extension, Command, find_packages
    from setuptools.command.install import install
    from setuptools.command.install_lib import install_lib as _install_lib
    from setuptools.command.build_ext import build_ext
    from setuptools.command.build_clib import build_clib as _build_clib
except:
    from distutils import setup, Extension, Command, find_packages
    from distutils.command.install import install
    from distutils.command.install_lib import install_lib as _install_lib
    from distutils.command.build_ext import build_ext
    from distutils.command.build_clib import build_clib as _build_clib

from numpy import get_include

with open("README.rst") as f:
    long_desc = f.read()
    ind = long_desc.find("\n")
    long_desc = long_desc[ind + 1:]

class install_lib(_install_lib):
    def run(self):
        env = os.environ.copy()
        subprocess.check_call(['make'], env=env)

#class build_clib(_build_clib):
#    def run(self):
#        self.announce("Building library files", level=3)
#        self.skip_build = True
#        env = os.environ.copy()
#        subprocess.check_call(['make'], env=env)

#class aepyInstall(install):
#    def run(self):
        #extdir = os.path.abspath(
        #    os.path.dirname('./aepy/'))
#	
#        env = os.environ.copy()
#        subprocess.check_call(['make'], env=env)
#
#        files = [os.path.join(extdir, fname) for fname in 
#                 os.listdir(extdir) if 
#                 os.path.isfile(os.path.join(extdir, fname))]
#	print('FILES:',files)
#        self.install_data = files
	#[os.path.join(self.install_data, fname)
        #                                for fname in files]
        #self.outfiles = self.distribution.data_files
#	install.run(self)

class MakeExtension(Extension):
    def __init__(self, name, sourcedir=''):
        Extension.__init__(self, name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)

class aepyBuildExt(build_ext):
    def run(self):
        buildflag = True
        if buildflag:
            ext = MakeExtension('_aepy', sourcedir='aepy/.'),
            self.my_build_extension(ext)

    def my_build_extension(self):
        env = os.environ.copy()
        if not os.path.exists(self.build_temp):
            os.makedirs(self.build_temp)
        subprocess.check_call(['make'], env=env)

        print()  # Add an empty line for cleaner output

VERSION = "0.0.1"
CLASSIFIERS = [
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.6",
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: GNU GPL",
    "Operating System :: OS Independent",
    "Topic :: Scientific/Engineering :: Physics",
    "Topic :: Scientific/Engineering :: Chemistry"
    "Topic :: Scientific/Engineering :: Material Science"
]
    
#aepy_module = Extension(
#		'_aepy',
#		sources = [],
#		#extra_objects = glob.glob(os.path.join(os.path.pardir,"aepy/*.so")),
#		#libraries = ['lapack', 'blas', 'gfortran']
#		)

setup(
    cmdclass= {
        #'build_ext'  : build_ext,
        #'build_clib'  : build_clib,
	'install_lib' : install_lib,
    },
    name="aepy",
    packages=find_packages('aepy'),
    version = VERSION,
    install_requires=["numpy>=1.5"],
    author = "Berk Onat",
    author_email = "B.Onat@warwick.ac.uk",
    maintainer="Berk Onat",
    url="https://github.com/berkonat/aepy.git",
    license="GNU GPL",
    description="Python Wrapper for AENET (Artificial Neural Network Potentials) Fortran Libraries",
    long_description=long_desc,
    classifiers = CLASSIFIERS,
    keywords=[],
    #libraries = [('', { 'sources' : ['aepy/_aepy.so']})],
    package_dir={'': 'aepy'},
    package_data={
	    '' : ['_aepy.so', 'aepy_fbind.py'],
	    'aepy': ['_aepy.so', 'aepy_fbind.py'],
	    },
    py_modules=['aepy'],
    #ext_modules = [MakeExtension('_aepy', sourcedir='aepy/.')],
    #ext_modules = [aepy_module],
    include_package_data=True
    )

