"""
.. module:: YUMLReady Diagram module
   :platform: Linux
   :synopsis: Module that implements the core of the YUMLReady library
   :copyright: (c) 2013 by Ernesto Bossi.
   :license: BSD.

.. moduleauthor:: Ernesto Bossi <bossi.ernestog@gmail.com>
"""
import inspect
from YUMLRules import *
from YUMLVisitor import YUMLVisitor

def createvarIfNotExists(obj, var, initial):
    try:
        getattr(obj, var)
    except AttributeError:
        setattr(obj, var, initial)

#Asociations
NOTE_ASSOCIATION = '-'
SIMPLE_ASSOCIATION = '->'
CARDINALITY = '..'
DIRECTIONAL_ASSOCIATION = '- >'
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

VALID_DIRECTIONS = [DIRECRTION_Right_to_Left, DIRECRTION_TopDown, DIRECTION_Left_to_Right]

#Scale
SCALE_HUGE = "scale:180"
SCALE_BIG = "scale:120"
SCALE_SMALL = "scale:80"
SCALE_TINY = "scale:60"
SCALE_NORMAL = ""

isValidScale = lambda (scale): scale in VALID_SCALES
VALID_SCALES = [SCALE_HUGE, SCALE_BIG, SCALE_SMALL, SCALE_TINY, SCALE_NORMAL]

VALID_COLORS = ["orange", "blue", "red", "black", "white", "brown", "magenta", "green", "pink", "violet", "grey"]


class YUMLDiagram(object):

    def __init__(self):
        self.direction = None
        self.scale = None
        self.classes = []
        self.relations = []
        self.notes = []
        self.comments = []

    def addNote(self, note):
        self.notes.append(YUMLNote(note))

    def setScale(self, scale):
        if isValidScale(scale):
            self.scale = None if scale == SCALE_NORMAL else scale

    def addRelation(self, relation):
        try:
            for relationship in self.relations:
                relationship.isSameRelation(relation)
            self.relations.append(relation.checkObjects(self))
        except ExistingRelationException:
            #returns as it's trying to enter an existing relation in the diagram
            return

    def checkObject(self, classObject):
        self.addClass(classObject)

    def addClass(self, classDeclaration):
        if not classDeclaration in self.classes:
            self.classes.append(YUMLClass(classDeclaration))

    def setDirection(self, direction):
        if not direction in VALID_DIRECTIONS:
            raise ValueError('Direction {0} is not a valid one.'.format(direction))
        self.direction = direction

    def materializeDiagram(self):
        YUMLVisitor().materializeDiagram(self)


class YUMLObject(object):

    def checkRules(self, rules):
        for rule in rules:
            rule().checkRule(self)

    def setBackground(self, background):
        if not background in VALID_COLORS:
            raise YUMLReadyException("Color {0} not in valid colors.".format(background))
        self.bg = background

    def convertToService(self):
        raise NotImplementedError


class YUMLConnector(YUMLObject):

    CONNECTOR_RULES = [NoteConnectionRule]

    def __init__(self, fromObject, ToObject, associationType):
        self.fromObject = fromObject
        self.association = associationType
        self.toObject = ToObject
        self.checkRules(self.CONNECTOR_RULES)

    def setAssociationType(self,association):
        self.association = association

    def setBackground(self, background):
        raise NotImplementedError

    def convertToService(self):
        return "[{0}]{1}[{2}]".format(self.fromObject,self.association,self.toObject)

    def checkObjects(self, diagram):
        diagram.checkObject(self.fromObject)
        diagram.checkObject(self.toObject)


class YUMLClass(YUMLObject):

    CLASS_RULES = [ReservedClassName]

    def __init__(self, classDeclaration):
        self.classDeclaration = classDeclaration
        self.introspectClass()
        self.checkRules(self.CLASS_RULES)

    def introspectClass(self):
        self.methods = inspect.getmembers(self.classDeclaration, predicate=inspect.ismethod)
        attributes = inspect.getmembers(self.classDeclaration, lambda a: not(inspect.isroutine(a)))
        self.attributes = [a for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))]
        self.className = self.classDeclaration.__name__

    def getAttributes(self):
        return '|' if not self.attributes else '|'+';'.join([attr[0] for attr in self.attributes])

    def getMethods(self):
        return '' if not self.methods else '|'+';'.join([method[0]+"()" for method in self.methods])

    def getClassName(self):
        createvarIfNotExists(self, 'bg', None)
        return self.className+"{bg:{0}}".format(self.bg) if self.bg else self.className

    def convertToService(self):
        return "[{0}{1}{2}]".format(self.getClassName(), self.getAttributes(), self.getMethods())


class YUMLNote(YUMLObject):

    def __init__(self, note):
        self.note = note

    def convertToService(self):
        return "[note: {0}{bg:{1}}]".format(self.note, self.bg) if self.bg else "[note: {0}]".format(self.note)


class YUMLComment(YUMLObject):

    def __init__(self, comment):
        self.comment = comment

    def setBackground(self, background):
        raise NotImplementedError

    def convertToService(self):
        return "// {0}".format(self.comment)

class YUMLReadyException(Exception): pass
class ExistingRelationException(YUMLReadyException): pass
