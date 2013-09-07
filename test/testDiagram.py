from unittest import TestCase
from YUMLConverter.YUMLDiagram import *
from TestingClassesRepo import *


class TestDiagram(TestCase):

    def setUp(self):
        self.diagram = YUMLDiagram()

    def testSettingClasses(self):
        self.diagram.add_class(CompleteClassTest)
        self.assertEqual(1, self.diagram.classes.__len__())
        print self.diagram.classes[0].convert_to_service()
