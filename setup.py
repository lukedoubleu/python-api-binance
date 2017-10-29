#!/usr/bin/env python

from distutils.core import setup


setup(name='python-binance-api',
      version='0.1.0',
      packages=['binanceapi'],
      modules=['api'],
      description='Python for Binance API',
      author='Luke Westfield',
	  url='https://github.com/lukedoubleu/python-binance-api'
	  keywords=['binance','crypto', 'cryptocurrency', 'exchange',
				'binance api', 'bitcoin']
      author_email='ldwestfield@protonmail.ch',
	  license='MIT License',
      classifiers=[
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: MIT License',
          'Development Status :: 4 - Beta',
          'Topic :: Office/Business :: Financial :: Cryptocurrency',
      ])