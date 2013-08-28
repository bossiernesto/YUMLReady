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
from lxml import etree
import io
from utils.cookieJar import YUMLCookieJar

def isObjOfType(obj,_type):
    return type(obj) in ([_type] + _type.__subclasses__())


class XPathExtractor(object):
    """
        Extractor using Xpath
    """

    def get_object(self, data):

        parser = etree.HTMLParser()
        memObj = io.StringIO if isObjOfType(data, unicode) else io.BytesIO
        html = etree.parse(memObj(data), parser)
        return html


class RequestHelper(object):

    def __init__(self):
        self.handlers = []
        self.handlers.append(YUMLCookieJar())

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
        self.visitor = None

    def postResource(self, url, data):
            return self.request.postContent(url, data)

    def getResource(self, url):
            return self.request.getResource().open(url)


class YUMLService(YUMLServiceAbstract):

    DRAW_URL = 'http://yuml.me/diagram/scruffy/class/draw'
    CLASS_PREFIX_URL = 'http://yuml.me/diagram/scruffy;/class'
    EDIT_LATER_LABEL = '/edit'
    FORMATS = {'PNG': '', 'JPEG': 'jpg', 'JPG': 'jpg', 'JSON': 'json', 'SVG': 'svg', 'PDF': 'pdf'}

    def buildDiagram(self, visitor,  shortUrl=False):
        self.cleanDiagram()
        self.visitor = visitor
        self.getShortUrl() if shortUrl else self.postDiagram(self.visitor.convertToService())

    def setUrlDiagram(self,url):
        self.urlDiagram = self.CLASS_PREFIX_URL + url

    def setDSLText(self, value):
        self.values = {'dsl_text': value}

    def cleanDiagram(self):
        self.postDiagram('')

    def postDiagram(self, value):
        self.setDSLText(value)
        return self.postResource(self.DRAW_URL, self.values).read()

    def getShortUrl(self):
        extractor = XPathExtractor().get_object(self.postDiagram(self.visitor.convertToService()))
        self.shortUrl = extractor.xpath('//*[@id="content"]/p[4]/a')
        return self.shortUrl

    def fetchFormat(self, format):
        if not self.visitor:
            raise Exception('Diagram not submitted')
        try:
            url = self.shortUrl if self.shortUrl else self.setUrlDiagram(self.visitor.convertToImport())
            return url + '.' + self.FORMATS[format]
        except AttributeError:
            raise Exception('Invalid type of format: {0}'.format(format))
