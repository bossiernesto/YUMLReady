"""
.. module:: YUMLReady Service
   :platform: Linux
   :synopsis:  Classes to interact with the YUML.me service
   :copyright: (c) 2013 by Ernesto Bossi.
   :license: BSD.

.. moduleauthor:: Ernesto Bossi <bossi.ernestog@gmail.com>
"""
import urllib2
import urllib
from YUMLDiagram import YUMLDiagram
from lxml import etree
import io

# Type checking


def isObjOfType(obj,_type):
    return type(obj) in ([_type] + _type.__subclasses__())


class XPathExtractor(object):
    """
        Extractor using Xpath
    """

    def get_object(self, data):

        parser = etree.HTMLParser()
        memObj= io.StringIO if isObjOfType(data, unicode) else io.BytesIO
        html = etree.parse(memObj(data), parser)
        return html


class RequestHelper(object):

    def __init__(self):
        self.handlers = []

    def setProxyHandler(self, user, password, proxy, port='80'):
        """Proxy hanlder"""
        handler = 'http://%s:%s@%s:%s' % (user, password, proxy, port)
        handlerAux = urllib2.ProxyHandler({'http': handler, 'https': handler})
        self.handlers.append(handlerAux)

    def buildOpenerWrapper(self, func, args):
            """Partial helper function"""
            return func(*args)

    def getResource(self):
        opener = self.buildOpenerWrapper(urllib2.build_opener, self.handlers)
        opener.addheaders = [('User-agent', 'Mozilla/6.0')]
        return opener

    def postContent(self, url, content):
        data = urllib.urlencode(content)
        req = urllib2.Request(url, data)
        return self.getResource().open(req)


class YUMLServiceAbstract(object):

    def __init__(self):
        self.request = RequestHelper()
        self.diagram = None

    def postResource(self, url, data):
            return self.request.postContent(url, data)

    def getResource(self, url):
            return self.request.getResource().open(url)

class YUMLService(YUMLServiceAbstract):

    DRAW_URL = 'http://yuml.me/diagram/scruffy/class/draw'
    CLASS_PREFIX_URL = 'http://yuml.me/diagram/scruffy;/class'
    EDIT_LATER_LABEL = '/edit'
    FORMATS = {'PNG': '', 'JPEG': 'jpg', 'JPG': 'jpg', 'JSON': 'json', 'SVG': 'svg', 'PDF': 'pdf'}

    def buildDiagram(self, diagram,  shortUrl=False):
        if not isinstance(diagram, YUMLDiagram):
            raise Exception('{0} is not an instance of {1}.'.format(diagram, YUMLDiagram.__name__))
        url = self.CLASS_PREFIX_URL
        #call visitor to populate all options
        self.urlDiagram = url

    def postDiragram(self):
        values = {'dsl_text': self.diagram.convertToService()}
        return self.postResource(self.DRAW_URL, values).read()

    def getShortUrl(self):
        extractor = XPathExtractor().get_object(self.postDiragram())
        self.shortUrl = extractor.xpath('//*[@id="content"]/p[4]/a')
        return self.shortUrl

    def fetchFormat(self, format):
        if not self.diagram:
            raise Exception('Diagram not submitted')
        try:
            url = self.shortUrl if self.shortUrl else self.urlDiagram
            return url + '.' + self.FORMATS[format]
        except AttributeError:
            raise Exception('Invalid type of format: {0}'.format(format))
