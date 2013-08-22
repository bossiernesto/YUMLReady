from unittest import TestCase
from YUMLConverter import YUMLConverter

#Example class used for testing
class A(object):

    def __init__(self):
        self.a=1
        self.j='AAAA'
        self.b='sss'

    def bleh(self):
        pass

    def jejeje(self):
        pass

class  testToYUML(TestCase):

    def setUp(self):
        self.converter=YUMLConverter()
        self.aClass=A
        self.aInstance=A()

