# -*- encoding: utf-8 -*-
from django.test import TestCase
from unit_field.units import Unit, UnitValue, get_choices

class UnitTest(TestCase):
    def test_attribute_factor(self):
        """
        the attribtue "factor" can be set
        """
        e = Unit(0.01, 'cm', 'centimetre')
        self.assertEqual(e.factor, 0.01)
        e.factor = 0.32
        self.assertEqual(e.factor, 0.32)

    def test_attribute_abbrev(self):
        """
        the attribtue "abbrev" can be set
        """
        e = Unit(0.01, u'cm', u'centimetre')
        self.assertEqual(e.abbrev, u'cm')
        e.abbrev = u'cm²'
        self.assertEqual(e.abbrev, u'cm²')

    def test_attribute_label(self):
        """
        the attribtue "label" can be set
        """
        e = Unit(0.01, u'cm', u'centimetre')
        self.assertEqual(e.label, u'centimetre')
        e.label = u'metre'
        self.assertEqual(e.label, u'metre')

class UnitValueTest(TestCase):
    def test_attribute_input(self):
        """
        the attribtue "input" can be set
        """
        e = UnitValue(7.1, 0.01)
        self.assertEqual(e.input, 7.1)
        e.input = 4
        self.assertEqual(e.input, 4)

    def test_attribute_unit(self):
        """
        the attribtue "input" can be set
        """
        e = UnitValue(7.1, 0.01)
        self.assertEqual(e.unit, 0.01)
        e.unit = 0.1
        self.assertEqual(e.unit, 0.1)

    def test_property_value(self):
        """
        the property "value" returns the user entered data (input)
        multiplied by the unit factor (unit)
        """
        testCases = [
            { 'params': [7.1, 0.1],  'result': 0.71 },
            { 'params': [0.1, 0.1],  'result': 0.01 },
            { 'params': [5, 0.01],   'result': 0.05 },
            { 'params': [2.4, 1000], 'result': 2400 },
        ]
        for testCase in testCases:
            uv = UnitValue(
                testCase['params'][0],
                testCase['params'][1])
            self.assertAlmostEqual(uv.value, testCase['result'], places=12)

    def test_get_choices(self):
        """
        checks if the method "get_choices" transforms the data
        in the correct way
        """
        a = [
            Unit(0.001, 'mm', 'milimetre' ),
            Unit(0.01,  'cm', 'centimetre'),
            Unit(0.1,   'dm', 'decimetre' ),
        ]

        b = [(0.001, 'mm'), (0.01, 'cm'), (0.1, 'dm')]
        self.assertEqual(get_choices(a), b)
