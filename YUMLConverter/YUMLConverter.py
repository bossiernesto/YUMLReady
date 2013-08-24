"""
.. module:: YUMLReady Converter
   :platform: Linux
   :synopsis: Module that implements the internal DSL to use with the YUMLReady library
   :copyright: (c) 2013 by Ernesto Bossi.
   :license: BSD.

.. moduleauthor:: Ernesto Bossi <bossi.ernestog@gmail.com>
"""
from YUMLDiagram import *


class YUMLConverter(object):

    def __init__(self):
        self.resetDiagram()

    def resetDiagram(self):
        self.diagram = YUMLDiagram()