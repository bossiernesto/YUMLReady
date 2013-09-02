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

    def define_class(self,class_declaration):
        if class_declaration not in self.definedClasses:
            to_append = class_declaration.convert_to_service()
            self.definedClasses.append(class_declaration)
            self.visitedObjects.append(class_declaration)
            return to_append
        return class_declaration.reduced_convert_to_service()

    def build_custom_connector(self, connector):
        return '{0}{1}{2}'.format(self.define_class(connector.fromObject),connector.association,self.define_class(connector.ToObject))

    def walk_comments(self):
        for comment in self.diagram.comments:
            self.diagramService += comment.convert_to_service()+'\n'
            self.visitedObjects.append(comment)

    def walk_connectors(self):
        for connector in self.diagram.connectors:
            if connector.fromObject in self.visitedObjects and connector.toObject in self.visitedObjects:
                self.diagramService += connector.convert_to_service()
            else:
                self.diagramService += self.build_custom_connector(connector)
            self.visitedObjects.append(connector)

    def walk_notes(self):
        for note in self.diagram.notes:
            if note not in self.definedClasses:
                self.diagramService += note.convert_to_service()+'\n'
                self.definedClasses.append(note)
                self.visitedObjects.append(note)
