from setuptools import setup

setup(name='pywikc',
      version='0.1.0',
      description='Warping-inclusive coupling and processing for finite elemet component macro models',
      url='https://github.com/ahartloper/WIKC',
      author='ahartloper',
      author_email='alexander.hartloper@epfl.ch',
      license='MIT',
      packages=['pywikc', 'pywikc.imperfections'],
      install_requires=[
          'numpy', 'pandas>=0.24.1'
      ],
      zip_safe=False)
