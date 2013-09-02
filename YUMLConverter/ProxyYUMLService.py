"""
.. module:: YUMLReady Service
   :platform: Linux
   :synopsis:  Classes to interact with the YUML.me service
   :copyright: (c) 2013 by Ernesto Bossi.
   :license: GPL v3.

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

    def set_proxy_handler(self, user, password, proxy, port='80'):
        """Proxy hanlder"""
        handler = 'http://%s:%s@%s:%s' % (user, password, proxy, port)
        handlerAux = urllib2.ProxyHandler({'http': handler, 'https': handler})
        self.handlers.append(handlerAux)

    def build_opener_wrapper(self, func, args):
            """Partial helper function"""
            return func(*args)

    def get_resource(self):
        opener = self.build_opener_wrapper(urllib2.build_opener, self.handlers)
        opener.addheaders = [('User-agent', 'Mozilla/6.0')]
        return opener

    def post_content(self, url, content):
        data = urllib.urlencode(content)
        req = urllib2.Request(url, data)
        return self.get_resource().open(req)


class YUMLServiceAbstract(object):

    def __init__(self):
        self.request = RequestHelper()
        self.visitor = None

    def post_resource(self, url, data):
            return self.request.post_content(url, data)

    def get_resource(self, url):
            return self.request.get_resource().open(url)


class YUMLService(YUMLServiceAbstract):

    DRAW_URL = 'http://yuml.me/diagram/scruffy/class/draw'
    CLASS_PREFIX_URL = 'http://yuml.me/diagram/scruffy;/class'
    EDIT_LATER_LABEL = '/edit'
    FORMATS = {'PNG': '', 'JPEG': 'jpg', 'JPG': 'jpg', 'JSON': 'json', 'SVG': 'svg', 'PDF': 'pdf'}

    def build_diagram(self, visitor,  shortUrl=False):
        self.clean_diagram()
        self.visitor = visitor
        self.get_short_url() if shortUrl else self.post_diagram(self.visitor.convert_to_service())

    def set_url_diagram(self, url):
        self.urlDiagram = self.CLASS_PREFIX_URL + url

    def set_DSL_text(self, value):
        self.values = {'dsl_text': value}

    def clean_diagram(self):
        self.post_diagram('')

    def post_diagram(self, value):
        self.set_DSL_text(value)
        return self.post_resource(self.DRAW_URL, self.values).read()

    def get_short_url(self):
        extractor = XPathExtractor().get_object(self.post_diagram(self.visitor.convert_to_service()))
        self.shortUrl = extractor.xpath('//*[@id="content"]/p[4]/a')
        return self.shortUrl

    def fetch_format(self, diagramFormat):
        if not self.visitor:
            raise Exception('Diagram not submitted')
        try:
            url = self.shortUrl if self.shortUrl else self.set_url_diagram(self.visitor.convert_to_import())
            return url + '.' + self.FORMATS[diagramFormat]
        except AttributeError:
            raise Exception('Invalid type of format: {0}'.format(diagramFormat))
