from unittest import TestCase
from YUMLConverter.YUMLReady import YUMLDiagram
from TestingClassesRepo import CompleteClassTest

class testToYUML(TestCase):

    def setUp(self):
        self.diagram = YUMLDiagram()
        self.aClass = CompleteClassTest
        self.aInstance = CompleteClassTest()

    def test_diagram_set(self):
        self.diagram.add_class(CompleteClassTest)
        print self.diagram.materialize_diagram()

