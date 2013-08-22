import urllib2
import urllib
from YUMLDiagram import YUMLDiagram

class RequestHelper(object):

    def __init__(self):
        self.handlers=[]

    def setProxyHandler(self, user, password, proxy, port='80'):
        """Proxy hanlder"""
        handler = 'http://%s:%s@%s:%s' %(user, password, proxy, port)
        handlerAux=urllib2.ProxyHandler({'http': handler, 'https': handler})
        self.handlers.append(handlerAux)

    def buildOpenerWrapper(self, func, args):
            """Partial helper function"""
            return func(*args)

    def getResource(self):
        opener = self.buildOpenerWrapper(urllib2.build_opener,self.handlers)
        opener.addheaders = [('User-agent', 'Mozilla/6.0')]
        return opener

    def postContent(self,url,content):
        data = urllib.urlencode(content)
        return urllib2.Request(url, data)

class YUMLServiceAbstract(object):

    def __init__(self):
        self.request = RequestHelper()
        self.diagram= None

    def getResource(self,url):
            return self.request.getResource().open(url)

class YUMLService(YUMLServiceAbstract):

    DRAW_URL = 'http://yuml.me/diagram/scruffy/class/draw'
    CLASS_PREFIX_URL = 'http://yuml.me/diagram/scruffy;/class'
    EDIT_LATER_LABEL= '/edit'
    FORMATS = {'PNG':'','JPEG':'jpg','JPG':'jpg','JSON':'json','SVG':'svg','PDF':'pdf'}

    def buildDiagram(self, diagram,  shortUrl = False):
        if not isinstance(diagram,YUMLDiagram):
            raise Exception('{0} is not an instance of {1}.'.format(diagram,YUMLDiagram.__name__))
        url = self.CLASS_PREFIX_URL

    def postDiragram(self):
        values = {'dsl_text' : self.diagram.convertToService()}
        self.request.postContent(self.DRAW_URL,values)

    def getShortUrl(self):
        pass

    def fecthFormat(self, format):
        if not self.diagram:
            raise Exception('Diagram not submitted')
        try:
            return '.'+self.FORMATS[format]
        except AttributeError:
            raise Exception('Invalid type of format: {0}'.format(format))
