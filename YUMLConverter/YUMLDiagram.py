"""
.. module:: YUMLReady Diagram module
   :platform: Linux
   :synopsis: Module that implements the core of the YUMLReady library
   :copyright: (c) 2013 by Ernesto Bossi.
   :license: GPL v3.

.. moduleauthor:: Ernesto Bossi <bossi.ernestog@gmail.com>
"""
import inspect
from YUMLConverter.YUMLRules import *
from YUMLConverter.YUMLVisitor import YUMLVisitor

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
AGGREGATION_WITH_NUMBER = lambda number: '<>-{0}>'.format(number)
AGGREGATION_WITH_NUMBERS = lambda number, otherNumber: '<>-{0}>{1}'.format(number, otherNumber)
COMPOSITION = lambda number: '++-{0}>'.format(number)
INHERITANCE = '^-'
INTERFACE_INHERITANCE = '^-.-'
DEPENDENCIES = lambda text: '{0} -.->'.format(text)

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

isValidScale = lambda scale: scale in VALID_SCALES
VALID_SCALES = [SCALE_HUGE, SCALE_BIG, SCALE_SMALL, SCALE_TINY, SCALE_NORMAL]

VALID_COLORS = ["orange", "blue", "red", "black", "white", "brown", "magenta", "green", "pink", "violet", "grey"]


class YUMLDiagram(object):

    def __init__(self):
        self.direction = None
        self.scale = None
        self.classes = []
        self.connectors = []
        self.notes = []
        self.comments = []

    def add_note(self, note):
        self.notes.append(YUMLNote(note))

    def set_scale(self, scale):
        if isValidScale(scale):
            self.scale = None if scale == SCALE_NORMAL else scale

    def add_relation(self, connector_var):
        try:
            for connector in self.connectors:
                connector.is_same_connector(connector_var)
            connector_var.check_objects(self)
            self.connectors.append(connector_var)
        except ExistingRelationException:
            #returns as it's trying to enter an existing relation in the diagram
            pass

    def check_object(self, classObject):
        self.add_class(classObject)

    def add_class(self, classDeclaration):
        if not classDeclaration in self.classes:
            self.classes.append(YUMLClass(classDeclaration))

    def set_direction(self, direction):
        if not direction in VALID_DIRECTIONS:
            raise ValueError('Direction {0} is not a valid one.'.format(direction))
        self.direction = direction

    def materialize_diagram(self):
        YUMLVisitor().materialize_diagram(self)


class YUMLObject(object):

    def check_rules(self, rules):
        for rule in rules:
            rule().checkRule(self)

    def set_background(self, background):
        if not background in VALID_COLORS:
            raise YUMLReadyException("Color {0} not in valid colors.".format(background))
        self.bg = background

    def convert_to_service(self):
        raise NotImplementedError


class YUMLConnector(YUMLObject):

    CONNECTOR_RULES = [NoteConnectionRule]

    def __init__(self, fromObject, ToObject, associationType):
        self.fromObject = fromObject
        self.association = associationType
        self.toObject = ToObject
        self.check_rules(self.CONNECTOR_RULES)

    def is_same_connector(self, connector):
        if self.fromObject == connector.fromObject and self.toObject == connector.toObject:
            raise ExistingRelationException('connector {0} is the same as {1}'.format(connector, self))

    def set_association_type(self, association):
        self.association = association

    def set_background(self, background):
        raise NotImplementedError

    def convert_to_service(self):
        return "[{0}]{1}[{2}]".format(self.fromObject.__name__, self.association, self.toObject.__name__)

    def check_objects(self, diagram):
        diagram.check_object(self.fromObject)
        diagram.check_object(self.toObject)


class YUMLClass(YUMLObject):

    CLASS_RULES = [ReservedClassName]

    def __init__(self, class_declaration, silent_init=True):
        self.class_declaration = class_declaration
        self.silent_init = silent_init
        self.introspect_class()
        self.check_rules(self.CLASS_RULES)

    getAttributes = lambda self, declaration: inspect.getmembers(declaration, lambda a: not(inspect.isroutine(a)))

    def introspect_class(self):
        self.methods = [method for method in inspect.getmembers(self.class_declaration, predicate=inspect.ismethod)]
        if self.silent_init:
            self.methods = [methods for methods in self.methods if methods[0] != '__init__']
        attributes = self.getAttributes(self.class_declaration) + self.getAttributes(self.class_declaration())
        self.attributes = [a for a in attributes if not(a[0].startswith('__') and a[0].endswith('__'))]
        self.className = self.class_declaration.__name__

    def get_attributes(self):
        return '|' if not self.attributes else '|'+';'.join([attr[0] for attr in self.attributes])

    def get_methods(self):
        return '' if not self.methods else '|'+';'.join([method[0]+"()" for method in self.methods])

    def get_class_name(self):
        createvarIfNotExists(self, 'bg', None)
        return self.className+"{bg:{0}}".format(self.bg) if self.bg else self.className

    def reduced_convert_to_service(self):
        return "[{0}]".format(self.get_class_name())

    def convert_to_service(self):
        return "[{0}{1}{2}]".format(self.get_class_name(), self.get_attributes(), self.get_methods())


class YUMLNote(YUMLObject):

    def __init__(self, note):
        self.note = note

    def convert_to_service(self):
        return "[note: {0}{bg:{1}}]".format(self.note, self.bg) if self.bg else "[note: {0}]".format(self.note)


class YUMLComment(YUMLObject):

    def __init__(self, comment):
        self.comment = comment

    def set_background(self, background):
        raise NotImplementedError

    def convert_to_service(self):
        return "// {0}".format(self.comment)


class YUMLReadyException(Exception):
    pass


class ExistingRelationException(YUMLReadyException):
    pass
