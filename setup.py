from setuptools import setup


APP_NAME = 'squarescity'
DESCRIPTION = open('README.txt').read()

setup(name=APP_NAME,
      version='1.0.0',
      license='BSD',
      description=DESCRIPTION,
      author='petraszd',
      author_email='petraszd@gmail.com',
      url='http://pyweek.org/e/petraszd-pw-12',
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: End Users/Desktop',
                   'Intended Audience :: Information Technology',
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.5',
                   'Programming Language :: Python :: 2.6',
                   'Programming Language :: Python :: 2.7',
                   'Topic :: Games/Entertainment :: Arcade'],
      install_requires=['cocos2d'])
