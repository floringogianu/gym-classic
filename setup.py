from setuptools import setup, find_packages
import sys
import os.path

# Don't import gym module here, since deps may not be installed
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'gym-classic'))

setup(name='gym_classic',
      version=0.2,
      description='Fast games for developing RL algorithms.',
      url='https://github.com/floringogianu/gym-fast-envs',
      author='Florin Gogianu',
      author_email='florin.gogianu@gmail.com',
      license='',
      packages=[package for package in find_packages()
                if package.startswith('gym')],
      zip_safe=False,
      )
