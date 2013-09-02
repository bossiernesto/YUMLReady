"""
.. module:: YUMLReady Diagram module
   :platform: Linux
   :synopsis: Module to check some rules of the diagram related objects
   :copyright: (c) 2013 by Ernesto Bossi.
   :license: GPL v3.

.. moduleauthor:: Ernesto Bossi <bossi.ernestog@gmail.com>
"""
import keyword


def areInstance(objects, klass):
    return all([isinstance(object, klass)for object in objects])


class YUMLRule(object):

    def checkRule(self, object):
        raise NotImplementedError


class NoteConnectionRule(YUMLRule):

    def checkRule(self, object):
        if areInstance([object.fromObject, object.toObject], YUMLNote) and object.associationType != NOTE_ASSOCIATION:
                object.set_association_type(NOTE_ASSOCIATION)

class ReservedClassName(YUMLRule):

    def checkRule(self, object):
        if keyword.iskeyword(object.className):
            raise YUMLReadyException("Class name {0} is a reserved one. Please change the name in your model".format(object.className))
