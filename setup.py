from setuptools import setup
from setuptools.extension import Extension
from Cython.Build import cythonize
import numpy

my_integrals = [Extension('slowquant.molecularintegrals.runMIcython',['slowquant/molecularintegrals/runMIcython.pyx'])]

setup(ext_modules=cythonize(my_integrals), include_dirs=[numpy.get_include()])
