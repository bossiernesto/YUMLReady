"""
.. module:: YUMLReady Converter
   :platform: Linux
   :synopsis: Module that implements the internal DSL to use with the YUMLReady library
   :copyright: (c) 2013 by Ernesto Bossi.
   :license: GPL v3.

.. moduleauthor:: Ernesto Bossi <bossi.ernestog@gmail.com>
"""
import sys
import string
from YUMLDiagram import YUMLDiagram, VALID_COLORS, YUMLClass,YUMLComment,YUMLNote,DIRECRTION_Right_to_Left,\
DIRECRTION_TopDown,DIRECTION_Left_to_Right,NOTE_ASSOCIATION,SIMPLE_ASSOCIATION,CARDINALITY,DIRECTIONAL_ASSOCIATION,AGGREGATION,AGGREGATION_WITH_NUMBER,\
AGGREGATION_WITH_NUMBERS,COMPOSITION,INHERITANCE,INTERFACE_INHERITANCE,DEPENDENCIES,SCALE_HUGE,SCALE_BIG,SCALE_SMALL,SCALE_TINY,SCALE_NORMAL

for color in VALID_COLORS:
    setattr(sys.modules[__name__],string.upper(color),color)

class YUMLConverter(object):

    def __init__(self):
        self.resetDiagram()

    def resetDiagram(self):
        self.diagram = YUMLDiagram()