# -*- coding: utf-8 -*-

class Unit(object):
    def __init__(self, factor, abbrev, label):
        self.factor = factor
        self.abbrev = abbrev
        self.label = label

class UnitValue(object):
    def __init__(self, input, unit):
        self.input = input
        self.unit = unit

    @property
    def value(self):
        return self.input * self.unit

class UnitValueCreator(object):
    def __init__(self, field):
        self.field = field
        self.input_field_name = "%s_input" % (self.field.name, )
        self.unit_field_name = "%s_unit" % (self.field.name, )
        self.value_field_name = "%s_value" % (self.field.name, )

    def __get__(self, instance, type=None):
        if instance is None:
            return self.field

    def __set__(self, instance, value):
        if isinstance(value, UnitValue):
            setattr(instance, self.input_field_name, value.votes)
            setattr(instance, self.unit_field_name, value.unit)
            setattr(instance, self.value_field_name, value.value)

def get_choices(units):
    """
    returns a list of tuples, diesplayed in the field widget
    """
    unit_choices = []
    for unit in units:
        unit_choices.append((unit.factor, unit.abbrev, ))

    return unit_choices

UNITS_LENGTH = [
    Unit(0.001, 'mm', 'milimetre' ),
    Unit(0.01,  'cm', 'centimetre'),
    Unit(0.1,   'dm', 'decimetre' ),
    Unit(1,     'm',  'metre'     ),
    Unit(1000,  'km', 'kilometre' ),
]

UNITS_SQUARE_MEASURE = [
    Unit(0.000001, 'mm²', 'square milimetre' ),
    Unit(0.0001,   'cm²', 'square centimetre'),
    Unit(0.01,     'dm²', 'square decimetre' ),
    Unit(1,        'm²',  'square metre'     ),
    Unit(100,      'a',   'square decametre' ),
    Unit(10000,    'ha',  'square hectometre'),
    Unit(1000000,  'km²', 'square kilometre' ),
]

UNITS_SOLID_MEASURE = [
    Unit(0.000000001, 'mm³',  'cubic milimetre' ),
    Unit(0.000001,    'cm³',  'cubic centimetre'),
    Unit(0.001,       'dm³',  'cubic decimetre' ),
    Unit(1,           'm³',   'cubic meter'     ),
    Unit(1000,        'dam³', 'cubic decametre' ),
    Unit(1000000,     'hm³',  'cubic hectometre'),
    Unit(1000000000,  'km³',  'cubic kilometre' ),
]

UNITS_MASS = [
    Unit(0.000001, 'µg',  'microgram'       ),
    Unit(0.001,    'mg',  'milligram'       ),
    Unit(1,        'g',   'gram'            ),
    Unit(100,      'dag', 'decagram'        ),
    Unit(1000,     'kg',  'kilogram'        ),
    Unit(1000000,  't',   'tonne'           ),
]

UNITS_TIME = [
    Unit(0.000001, 'µg',  'microsecond' ),
    Unit(0.001,    'ms',  'millisecond' ),
    Unit(1,        's',   'second'      ),
    Unit(60,       'min', 'minute'      ),
    Unit(3600,     'h',   'hour'        ),
    Unit(86400,    'd',   'day'         ),
]

UNITS_ELECTRIC_CURRENT = [
    Unit(0.000001, 'µA', 'microampere'  ),
    Unit(0.001,    'mA', 'milliampere'  ),
    Unit(1,        'A',  'ampere'       ),
    Unit(1000,     'kA', 'kiloampere'   ),
]

UNITS_TEMPERATURE = [
    Unit(1,        'K',  'kelvin'       ),
]

UNITS_AMOUNT_OF_SUBSTANCE = [
    Unit(1,        'mol', 'mole'        ),
]

UNITS_LUMINOUS_INTENSITY = [
    Unit(1,        'cd', 'candela'      ),
]

UNITS_LENGTH_CHOICES = get_choices(UNITS_LENGTH)
UNITS_SQUARE_MEASURE_CHOICES = get_choices(UNITS_SQUARE_MEASURE)
UNITS_SOLID_MEASURE_CHOICES = get_choices(UNITS_SOLID_MEASURE)
UNITS_MASS_CHOICES = get_choices(UNITS_MASS)
UNITS_TIME_CHOICES = get_choices(UNITS_TIME)
UNITS_ELECTRIC_CURRENT_CHOICES = get_choices(UNITS_ELECTRIC_CURRENT)
UNITS_TEMPERATURE_CHOICES = get_choices(UNITS_TEMPERATURE)
UNITS_AMOUNT_OF_SUBSTANCE_CHOICES = get_choices(UNITS_AMOUNT_OF_SUBSTANCE)
UNITS_LUMINOUS_INTENSITY_CHOICES = get_choices(UNITS_LUMINOUS_INTENSITY)
