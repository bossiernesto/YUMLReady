"""
.. module:: YUMLReady Diagram module
   :platform: Linux
   :synopsis: Module that implements the core of the YUMLReady library
   :copyright: (c) 2013 by Ernesto Bossi.
   :license: BSD.

.. moduleauthor:: Ernesto Bossi <bossi.ernestog@gmail.com>
"""
from YUMLDiagram import *

class YUMLVisitor(object):

    def __init__(self):
        self.visitedObjects = []
        self.definedClasses = []

    def materializeDiagram(self,diagram):
        if not isinstance(diagram,YUMLDiagram):
            raise YUMLReadyException("Diagram {0} is not an instance of {1}".format(diagram,YUMLDiagram.__name__))
