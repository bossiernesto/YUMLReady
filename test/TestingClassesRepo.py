class CompleteClassTest(object):
    """
    Example class used for testing that has attributes and methods
    """

    def __init__(self):
        self.a = 1
        self.j = 'AAAA'
        self.b = 'sss'

    def method1(self):
        pass

    def anotherMethod(self):
        pass

    def methodWithArgument(self, argument4):
        pass


class EmptyClassTest(object):
    """
    Example Class use for testing
    """
    pass


class MethodOnlyClassTest(object):
    """
    Example Class use for testing, that only yields methods
    """

    def method2(self):
        pass

    def methodWithArguments(self, argument):
        pass


class AttributeOnlyClassTest(object):
    """
    Example Class use for testing, that only yields attributes
    """

    def __init__(self):
        self.attribute1 = "1"
        self.attribute2 = "2"