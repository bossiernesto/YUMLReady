"""
.. module:: YUMLReady Diagram module
   :platform: Linux
   :synopsis: Module that implements the core of the YUMLReady library
   :copyright: (c) 2013 by Ernesto Bossi.
   :license: BSD.

.. moduleauthor:: Ernesto Bossi <bossi.ernestog@gmail.com>
"""
import inspect

#Asociations
SIMPLE_AsSOCIATION = '->'
CARDINALITY = '..'
DIRECTIONAL_ASsOCIATION = '- >'
AGGREGATION = '+->'
AGGREGATION_WITH_NUMBER = lambda(number): '<>-{0}>'.format(number)
AGGREGATION_WITH_NUMBERS = lambda(number, otherNumber): '<>-{0}>{1}'.format(number, otherNumber)
COMPOSITION = lambda (number): '++-{0}>'.format(number)
INHERITANCE = '^-'
INTERFACE_INHERITANCE = '^-.-'
DEPENDENCIES = lambda (text): '{0} -.->'.format(text)

#Directions
DIRECTION_Left_to_Right = 'LR'
DIRECRTION_TopDown = 'TB'
DIRECRTION_Right_to_Left = 'RL'

isValidDirection = lambda (direction): direction in VALID_DIRECTIONS
VALID_DIRECTIONS = [DIRECRTION_Right_to_Left, DIRECRTION_TopDown, DIRECTION_Left_to_Right]

#Scale
SCALE_HUGE = "scale:180"
SCALE_BIG = "scale:120"
SCALE_SMALL = "scale:80"
SCALE_TINY = "scale:60"
SCALE_NORMAL = ""

isValidScale = lambda (scale): scale in VALID_SCALES
VALID_SCALES = [SCALE_HUGE, SCALE_BIG, SCALE_SMALL, SCALE_TINY, SCALE_NORMAL]


class YUMLDiagram(object):

    def __init__(self):
        self.direction = None
        self.size = None
        self.classes = []
        self.notes = []

    def setNote(self, note):
        self.notes.append(YUMLNote(note))

    def setSize(self, size):
        pass

    def setClass(self, klass):
        self.classes.append(YUMLClass(klass))

    def setDirection(self, direction):
        if not direction in VALID_DIRECTIONS:
            raise ValueError('Direction {0} is not a valid one.'.format(direction))
        self.direction = direction


class YUMLObject(object):

    def setBackground(self, background):
        self.bg = background

    def convertToService(self):
        raise NotImplementedError


class YUMLClass(object):

    def __init__(self, klass):
        self.klass = klass
        self.introspectClass()

    def introspectClass(self):
        self.methods = inspect.getmembers(self.klass, predicate=inspect.ismethod)
        attributes = inspect.getmembers(self.klass, lambda a: not(inspect.isroutine(a)))
        self.attributes = [a for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))]
        self.className = self.klass.__name__


class YUMLNote(YUMLObject):

    def __init__(self, note):
        self.note = note

    def convertToService(self):
        return "[note: {0}{bg:{1}}]".format(self.note, self.bg) if self.bg else "[note: {0}]".format(self.note)


class YUMLComment(YUMLObject):

    def __init__(self, comment):
        self.comment = comment

    def convertToService(self):
        return "// {0}".format(self.comment)