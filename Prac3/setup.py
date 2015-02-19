from distutils.core import setup, Extension

module1 = Extension('alg3',
                    sources = ['alg3.c'])

setup (name = 'alg3',
       version = '1.0',
       description = 'This is a demo package',
       ext_modules = [module1])
