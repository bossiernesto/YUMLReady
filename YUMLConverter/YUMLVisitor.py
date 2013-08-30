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

    def materialize_diagram(self, diagram):
        if not isinstance(diagram, YUMLDiagram):
            raise YUMLReadyException("Diagram {0} is not an instance of {1}".format(diagram, YUMLDiagram.__name__))
        self.diagram = diagram
        self.service.build_diagram(self)

    def convert_to_import(self):
        self.diagramImport = self.convert_to_service().replace('\n', ', ')

    def convert_to_service(self):
        self.walk_comments()
        self.walk_connectors()
        return self.diagramService

    def walk_comments(self):
        for comment in self.diagram.comments:
            self.diagramService += comment.convert_to_service()+'\n'
            self.visitedObjects.append(comment)

    def walk_connectors(self):
        pass

    def walk_notes(self):
        for note in self.diagram.notes:
            if note not in self.definedClasses:
                self.diagramService += note.convert_to_service()+'\n'
                self.definedClasses.append(note)
                self.visitedObjects.append(note)
