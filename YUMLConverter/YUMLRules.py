from YUMLDiagram import YUMLNote,NOTE_ASSOCIATION,YUMLReadyException
import keyword

def areInstance(objects, klass):
    return all([isinstance(object, klass)for object in objects])


class YUMLRule(object):

    def checkRule(self, object):
        raise NotImplementedError


class NoteConnectionRule(YUMLRule):

    def checkRule(self, object):
        if areInstance([object.fromObject,object.toObject],YUMLNote) and object.associationType != NOTE_ASSOCIATION:
                object.setAssociationType(NOTE_ASSOCIATION)

class ReservedClassName(YUMLRule):

    def checkRule(self, object):
        if keyword.iskeyword(object.className):
            raise YUMLReadyException("Class name {0} is a reserved one. Please change the name in your model".format(object.className))
