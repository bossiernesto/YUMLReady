from YUMLConverter.ProxyYUMLService import YUMLService
from unittest import TestCase


class testYUMLService(TestCase):

    def setUp(self):
        self.serviceGateway = YUMLService()