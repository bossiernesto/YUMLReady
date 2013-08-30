from unittest import TestCase
from YUMLConverter.YUMLReady import YUMLConverter


class testToYUML(TestCase):

    def setUp(self):
        self.converter = YUMLConverter()
        self.aClass = A
        self.aInstance = A()

