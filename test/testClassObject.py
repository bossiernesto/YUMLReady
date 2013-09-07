import unittest
from TestingClassesRepo import AttributeOnlyClassTest, CompleteClassTest
from YUMLConverter.YUMLDiagram import YUMLClass


class testClassObject(unittest.TestCase):

    def setUp(self):
        self.complete_object = YUMLClass(CompleteClassTest)
        self.attribute_only_object = YUMLClass(AttributeOnlyClassTest)

    def test_attribute_only_members(self):
        self.assertEqual(2, len(self.attribute_only_object.attributes))

    def test_complete_members(self):
        self.assertEqual(3, len(self.complete_object.attributes))
        self.assertEqual(3, len(self.complete_object.methods))
        self.complete_object = YUMLClass(CompleteClassTest, silent_init=False)
        self.assertEqual(4, len(self.complete_object.methods))

    def test_attribute_only_class_name(self):
        self.assertEqual(AttributeOnlyClassTest.__name__, self.attribute_only_object.get_class_name())

    def test_complete_class_name(self):
        self.assertEqual(CompleteClassTest.__name__, self.complete_object.get_class_name())

    def test_reduced_getService(self):
        for klass, instance in [(CompleteClassTest, self.complete_object),
                                (AttributeOnlyClassTest, self.attribute_only_object)]:
            self.assertEqual("[{0}]".format(klass.__name__), instance.reduced_convert_to_service())

    def test_attribute_only_service(self):
        self.assertEqual('[AttributeOnlyClassTest|attribute1;attribute2]',
                         self.attribute_only_object.convert_to_service())

    def test_complete_service(self):
        self.assertEqual('[CompleteClassTest|a;b;j|anotherMethod();method1();methodWithArgument()]',
                         self.complete_object.convert_to_service())