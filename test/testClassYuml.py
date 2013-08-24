from unittest import TestCase
from YUMLConverter.YUMLConverter import YUMLConverter


class A(object):
    """
    Example class used for testing
    """
    def __init__(self):
        self.a = 1
        self.j = 'AAAA'
        self.b = 'sss'

    def method1(self):
        pass

    def anotherMethod(self):
        pass


class testToYUML(TestCase):

    def setUp(self):
        self.converter = YUMLConverter()
        self.aClass = A
        self.aInstance = A()

