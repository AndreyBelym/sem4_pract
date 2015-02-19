from distutils.core import setup, Extension

module1 = Extension('alg1',
                    sources = ['alg1.c'])

setup (name = 'alg1',
       version = '1.0',
       description = 'This is a demo package',
       ext_modules = [module1])
