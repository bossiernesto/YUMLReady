"""
.. module:: YUMLReady Cookie
   :platform: Linux
   :synopsis: small and simple cookie wrapper
   :copyright: (c) 2013 by Ernesto Bossi.
   :license: BSD.

.. moduleauthor:: Ernesto Bossi <bossi.ernestog@gmail.com>
"""
import cookielib
import os.path
import urllib2
import tempfile

class YUMLCookieJar(urllib2.HTTPCookieProcessor):
    """ Cookie jar Class"""

    COOKIES_FILE = "yuml_cookies"

    def _make_temp_file(self):
        tmp = tempfile.gettempdir()
        self.cookie_file = os.path.join(tmp, self.COOKIES_FILE)

    def __init__ (self,blockeddoms=None,*args,**kwargs):
        """ Class initializer """
        self._make_temp_file()
        self.blockeddomains=blockeddoms
        self.policy=cookielib.DefaultCookiePolicy(blocked_domains=self.blockeddomains,
            strict_ns_domain=cookielib.DefaultCookiePolicy.DomainLiberal,rfc2965=True)
        self.jar=cookielib.LWPCookieJar(self.cookie_file,policy=self.policy)
        urllib2.HTTPCookieProcessor.__init__(self,self.jar,*args,**kwargs)

    def save_file(self):
        if self.jar is not None:
            self.jar.save(self.cookie_file)

    def load_file(self,force=False):

        if force:
            self.clean()

        if os.path.isfile(self.jar):
            self.jar.load()

    def clean(self):
        self.jar.clear()
