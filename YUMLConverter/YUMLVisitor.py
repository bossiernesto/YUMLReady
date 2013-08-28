"""
.. module:: YUMLReady Diagram module
   :platform: Linux
   :synopsis: Module that implements the core of the YUMLReady library
   :copyright: (c) 2013 by Ernesto Bossi.
   :license: BSD.

.. moduleauthor:: Ernesto Bossi <bossi.ernestog@gmail.com>
"""
from YUMLDiagram import *
from ProxyYUMLService import YUMLService

class YUMLVisitor(object):

    def __init__(self):
        self.visitedObjects = []
        self.definedClasses = []
        self.diagramService = ''
        self.diagramImport = ''
        self.service = YUMLService()

    def materializeDiagram(self,diagram):
        if not isinstance(diagram,YUMLDiagram):
            raise YUMLReadyException("Diagram {0} is not an instance of {1}".format(diagram,YUMLDiagram.__name__))
        self.diagram = diagram
        self.service.buildDiagram(self)

    def convertToImport(self):
        self.diagramImport = self.convertToService().replace('\n',', ') #TODO: replace las ', ' for a ''

    def convertToService(self):
        self.walkComments()
        self.walkConnectors()
        return self.diagramService

    def walkComments(self):
        for comment in self.diagram.comments:
            self.diagramService += comment.convertToService()+'\n'
            self.visitedObjects.append(comment)

    def walkConnectors(self):
        pass

    def walkNotes(self):
        for note in self.diagram.notes:
            if note not in self.definedClasses:
                self.diagramService += note.convertToService()+'\n'
                self.definedClasses.append(note)
                self.visitedObjects.append(note)
