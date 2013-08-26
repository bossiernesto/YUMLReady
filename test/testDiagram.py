from unittest import TestCase
from YUMLConverter.YUMLDiagram import *

class TestDiagram(TestCase):

    def setUp(self):
        self.diagram = YUMLDiagram()

    def prepareCommonDiagram(self):
        """
        // Cool Class Diagram
        [Customer]<>-orders*>[Order]
        [Order]++-0..*>[LineItem]
        [Order]-[note:Aggregate root.]
        """
        pass

