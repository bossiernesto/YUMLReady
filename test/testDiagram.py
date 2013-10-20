from unittest import TestCase
from YUMLConverter.YUMLDiagram import *
from TestingClassesRepo import *


class TestDiagram(TestCase):
    def setUp(self):
        self.diagram = YUMLDiagram()

    def test_setting_classes(self):
        self.diagram.add_class(CompleteClassTest)
        self.assertEqual(1, self.diagram.classes.__len__())
        self.assertEqual('[CompleteClassTest|a;b;j|anotherMethod();method1();methodWithArgument()]',
                         self.diagram.classes[0].convert_to_service())

    def test_setting_atrtribute_only_class(self):
        self.diagram.add_class(EmptyClassTest)
        self.assertEqual(1, self.diagram.classes.__len__())
        self.assertEqual('[EmptyClassTest|]', self.diagram.classes[0].convert_to_service())

    def test_setting_empty_class(self):
        self.diagram.add_class(AttributeOnlyClassTest)
        self.assertEqual('[AttributeOnlyClassTest|attribute1;attribute2]', self.diagram.classes[0].convert_to_service())