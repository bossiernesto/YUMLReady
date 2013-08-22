
#Asociations
SIMPLE_AsSOCIATION = '->'
CARDINALITY = '..'
DIRECTIONAL_ASsOCIATION = '- >'
AGGREGATION = '+->'
AGGREGATION_WITH_NUMBER = lambda(number): '<>-{0}>'.format(number)
AGGREGATION_WITH_NUMBERS = lambda(number,otherNumber): '<>-{0}>{1}'.format(number,otherNumber)
COMPOSITION = lambda (number): '++-{0}>'.format(number)
INHERITANCE = '^-'
INTERFACE_INHERITANCE = '^-.-'
DEPENDENCIES = lambda (text): '{0} -.->'.format(text)

#Directions
DIRECTION_Left_to_Right = 'LR'
DIRECRTION_TopDown = 'TB'
DIRECRTION_Right_to_Left = 'RL'

VALID_DIRECTIONS = [DIRECRTION_Right_to_Left,DIRECRTION_TopDown,DIRECTION_Left_to_Right]

class YUMLDiagram(object):

    def __init__(self):
        self.direction = None
        self.size = None
        self.classes = []
        self.notes = []

    def setNote(self,note):
        self.notes.append(YUMLNote().setNote(note))

    def setSize(self, size):
        pass

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
    pass

class YUMLNote(YUMLObject):

    def setNote(self,note):
        self.note = note

    def convertToService(self):
        return "[note: {0}{bg:{1}}]".format(self.note,self.bg) if self.bg else "[note: {0}]".format(self.note)
