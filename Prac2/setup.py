from distutils.core import setup, Extension

module1 = Extension('alg2',
                    sources = ['alg2.c'])

setup (name = 'alg2',
       version = '1.0',
       description = 'This is a demo package',
       ext_modules = [module1])
