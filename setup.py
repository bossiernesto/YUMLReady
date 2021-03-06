from setuptools import setup, find_packages
import os

PATH = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(PATH, ".")
templates_files = [os.path.join(templates_dir, file) for file in os.listdir(templates_dir)]

setup(name='YUMLReady',
      version='0.1',
      description='Small interface to YUML to build class diagrams from code or project',
      author='Ernesto Bossi',
      author_email='bossi.ernestog@gmail.com',
      license='BSD',
      keywords='class diagram',
      packages=find_packages(exclude=["test"]),
      data_files=[
          (templates_dir, templates_files)
      ],
      install_requires=['lxml']
)
