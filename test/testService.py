from YUMLConverter.ProxyYUMLService import YUMLService
from unittest import TestCase
from TestingClassesRepo import MethodOnlyClassTest
from YUMLConverter.YUMLDiagram import YUMLClass


class testYUMLService(TestCase):
    def setUp(self):
        self.serviceGateway = YUMLService()
        self.class_to_set = MethodOnlyClassTest
        self.diagram = YUMLClass(self.class_to_set).convert_to_service()

    def test_service(self):
        self.serviceGateway.post_diagram(self.diagram)
