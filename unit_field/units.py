# -*- coding: utf-8 -*-
from django.utils import formats
from django.utils.translation import ugettext_lazy as _
import math

def _label(_input, _unit):
    _input = formats.localize(_input, use_l10n=True)
    return u'%s %s' % (_input, _unit)

def convert_unit(value, units, unit_id_in, unit_id_out):
    # if units are identical
    if unit_id_in == unit_id_out:
        return value

    #retrieve conversion factors
    for unit in units:
        if unit.id == unit_id_in:
            f1 = unit.factor
        if unit.id == unit_id_out:
            f2 = unit.factor

    return value * f1 / f2

class Unit(object):
    def __init__(self, id, abbrev, label, factor=None, to_base_function=None):
        self.id  = id
        self.abbrev = abbrev
        self.label = label
        self.to_base_function = to_base_function
        if factor is None:
            self.factor = id
        else:
            self.factor = factor

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
        unit_choices.append((unit.id, unit.abbrev, ))

    return unit_choices

UNITS_PERCENTAGE = [
    Unit(u'%',      _(u'%'),    _(u'Percent'),      0.01),
    Unit(u'1',      _(u'1'),    _(u'Whole'),        1.0),
]

UNITS_VISCOSITY = [
    # Unit(u'kg/ms',   _(u'kg/ms'),   _(u'kg/ms' ),   1, ),
    Unit(u'm²/s',   _(u'm²/s'),   _(u'm²/s' ),    1, ),
    Unit(u'mm²/s',   _(u'mm²/s'),   _(u'mm²/s' ), 0.000001, ),
]

UNITS_LENGTH = [
    Unit(u'μm',   _(u'μm'),   _(u'micrometre'),   0.000001, ),
    Unit(u'mm',   _(u'mm'),   _(u'milimetre' ),   0.001, ),
    Unit(u'cm',   _(u'cm'),   _(u'centimetre'),   0.01,  ),
    Unit(u'dm',   _(u'dm'),   _(u'decimetre' ),   0.1,   ),
    Unit(u'm',    _(u'm'),    _(u'metre'     ),   1,     ),
    Unit(u'km',   _(u'km'),   _(u'kilometre' ),   1000,  ),
]

UNITS_LENGTH_SMALL = [
    Unit(u'μm',   _(u'μm'),   _(u'micrometre'),  0.000001, ),
    Unit(u'nm',   _(u'nm'),   _(u'nanometre'),   0.000000001,  ),
    Unit(u'pm',   _(u'pm'),   _(u'pikometre'),   0.000000000001,   ),
]

UNITS_LENGTH_BRITISH = [
    Unit(u'in',   _(u'"'),   _(u'inch' ),      0.0254, ),
    Unit(u'ft',   _(u'ft'),  _(u'feet'),       0.3048, ),
    Unit(u'sm',   _(u'sm'),  _(u'sm' ),     1852.0,    ),
    Unit(u'mi',   _(u'mi'),  _(u'mi' ),     1609.344,  ),
]

UNITS_LENGTH_SCIENCE = [
    Unit(u'AE',   _(u'AE'),   _(u'Astronomische Einheit' ), 149597870691, ),
]

UNITS_SQUARE_MEASURE = [
    Unit(u'mm²',  _(u'mm²'),  _(u'square milimetre'),  0.000001, ),
    Unit(u'cm²',  _(u'cm²'),  _(u'square centimetre'), 0.0001,   ),
    Unit(u'dm²',  _(u'dm²'),  _(u'square decimetre'),  0.01,     ),
    Unit(u'm²',   _(u'm²'),   _(u'square metre'),      1,        ),
    Unit(u'a',    _(u'a'),    _(u'square decametre'),  100,      ),
    Unit(u'ha',   _(u'ha'),   _(u'square hectometre'), 10000,    ),
    Unit(u'km²',  _(u'km²'),  _(u'square kilometre'),  1000000,  ),
]

UNITS_SOLID_MEASURE = [
    Unit(u'mm³',  _(u'mm³'),  _(u'cubic milimetre') ,  0.000000001, ),
    Unit(u'cm³',  _(u'cm³'),  _(u'cubic centimetre'),  0.000001,    ),
    Unit(u'dm³',  _(u'dm³'),  _(u'cubic decimetre'),   0.001,       ),
    Unit(u'm³',   _(u'm³'),   _(u'cubic meter'),       1,           ),
    Unit(u'dam³', _(u'dam³'), _(u'cubic decametre'),   1000,        ),
    Unit(u'hm³',  _(u'hm³'),  _(u'cubic hectometre'),  1000000,     ),
    Unit(u'km³',  _(u'km³'),  _(u'cubic kilometre'),   1000000000,  ),
    Unit(u'l',    _(u'l'),    _(u'litre'),             0.001,       ),
]

UNITS_MASS = [
    Unit(u'µg',   _(u'µg'),   _(u'microgram'),     0.000001,   ),
    Unit(u'mg',   _(u'mg'),   _(u'milligram'),     0.001,      ),
    Unit(u'g',    _(u'g'),    _(u'gram')     ,     1,          ),
    Unit(u'dag',  _(u'dag'),  _(u'decagram') ,     100,        ),
    Unit(u'kg',   _(u'kg'),   _(u'kilogram') ,     1000,       ),
    Unit(u't',    _(u't'),    _(u'tonne')    ,     1000000,    ),
]

UNITS_TIME = [
    Unit(u'µs',  _(u'µs'),  _(u'microseconds'), 0.000001, ),
    Unit(u'ms',  _(u'ms'),  _(u'millisecond'),  0.001,    ),
    Unit(u's',   _(u's'),   _(u'second'),       1,        ),
    Unit(u'min', _(u'min'), _(u'minute'),       60,       ),
    Unit(u'h',   _(u'h'),   _(u'hour'),         3600,     ),
    Unit(u'd',   _(u'd'),   _(u'day'),          86400,    ),
]

UNITS_TIME2 = [
    Unit(u'Hours',     _(u'Hours'),     _(u'Hours'),         1, ),
    Unit(u'Days',      _(u'Days'),      _(u'Days'),         24, ),
    Unit(u'Weeks',     _(u'Weeks'),     _(u'Weeks'),       168, ),
    Unit(u'Months',    _(u'Months'),    _(u'Months'),      720, ),
    Unit(u'Semesters', _(u'Semesters'), _(u'Semesters'),  4320, ),
    Unit(u'Years',     _(u'Years'),     _(u'Years'),      8760, ),
]

UNITS_ELECTRIC_CURRENT = [
    Unit(u'µA',  _(u'µA'),  _(u'microampere'),  0.000001, ),
    Unit(u'mA',  _(u'mA'),  _(u'milliampere'),  0.001,    ),
    Unit(u'A',   _(u'A'),   _(u'ampere')     ,  1,        ),
    Unit(u'kA',  _(u'kA'),  _(u'kiloampere') ,  1000,     ),
]

UNITS_TEMPERATURE = [
    #Unit(u'K',      _(u'K'),     _(u'kelvin'),   1 ),
    Unit(u'°C',     _(u'°C'),    _(u'degree'),   1.0),
    Unit(u'°F',     _(u'°F'),    _(u'fahrenheit'), 0.0,
        to_base_function=lambda x: (x - 32.0) / 1.8),
]

UNITS_AMOUNT_OF_SUBSTANCE = [
    Unit(u'mol',    _(u'mol'),  _(u'mole'),     1 ),
]

UNITS_LUMINOUS_INTENSITY = [
    Unit(u'cd',     _(u'cd'),   _(u'candela'),  1 ),
]

# base units (SI system)

UNITS_LENGTH_CHOICES = get_choices(UNITS_LENGTH)
UNITS_SQUARE_MEASURE_CHOICES = get_choices(UNITS_SQUARE_MEASURE)
UNITS_SOLID_MEASURE_CHOICES = get_choices(UNITS_SOLID_MEASURE)
UNITS_MASS_CHOICES = get_choices(UNITS_MASS)
UNITS_TIME_CHOICES = get_choices(UNITS_TIME)
UNITS_TIME2_CHOICES = get_choices(UNITS_TIME2)
UNITS_ELECTRIC_CURRENT_CHOICES = get_choices(UNITS_ELECTRIC_CURRENT)
UNITS_TEMPERATURE_CHOICES = get_choices(UNITS_TEMPERATURE)
UNITS_AMOUNT_OF_SUBSTANCE_CHOICES = get_choices(UNITS_AMOUNT_OF_SUBSTANCE)
UNITS_LUMINOUS_INTENSITY_CHOICES = get_choices(UNITS_LUMINOUS_INTENSITY)

# derived units

UNITS_ANGLE = [
    Unit(u'rad',    _(u'rad'),    _(u'Radians'),  1.0 ),
    Unit(u'deg',    _(u'°'),      _(u'Degrees'),  math.pi / 180.0 ),
    # Unit(u'grad',   _(u'grad'),   _(u'Grads'),    math.pi / 200 ),
    Unit(u'arcmin', _(u'arcmin'), _(u'arcmin'),  math.pi / (180.0 * 60.0) ),
    Unit(u'arcsec', _(u'arcsec'), _(u'arcsec'),  math.pi / (180.0 * 60.0 * 60.0) ),
    Unit(u'rotation', _(u'rot.'), _(u'rot.'), 2.0 * math.pi),
]

UNITS_DENSITY = [
    Unit(u'kg/m³',    _(u'kg/m³'),    _(u'kg/m³'),     1 ),
    Unit(u'kg/dm³',   _(u'kg/dm³'),   _(u'kg/dm³'),    1000 ),
]

UNITS_FORCE = [
    Unit(u'N',   _(u'N'),   _(u'Newton'),    1 ),
    Unit(u'kN',   _(u'kN'),   _(u'Kilonewton'),    1000 ),
]

UNITS_SPEED = [
    Unit(u'1/min',   _(u'1/min'),   _(u'rotation per minute'),    1 ),
]

UNITS_TORQUE = [
    Unit(u'Nm',   _(u'Nm'),   _(u'Newtonmeter'),    1 ),
]

UNITS_VELOCITY = [
    Unit(u'mm/s',   _(u'mm/s'),   _(u'milimetres per second'),  0.001 ),
    Unit(u'm/s',    _(u'm/s'),    _(u'metres per second'),      1.0 ),
    Unit(u'm/min',  _(u'm/min'),  _(u'metres per minute'),      1.0 / 60.0 ),
    Unit(u'km/h',   _(u'km/h'),   _(u'kilometres per hour'),    1.0 / 3.6 ),
]

UNITS_ACCELERATION = [
    Unit(u'm/s²',  _(u'm/s²'),  _(u'm/s²'),     1),
]

UNITS_CURRENT = [
    Unit(u'mA',     _(u'mA'),  _(u'milli ampere'),  0.001),
    Unit(u'A',      _(u'A'),    (u'ampere'),        1),
]

UNITS_POTENTIAL = [
    Unit(u'V',      _(u'V'),  _(u'volt'),  1),
]

UNITS_JERK = [
    Unit(u'm/s³',   _(u'm/s³'),     _(u'm/s³'),     1),
]

UNITS_SNAP = [
    Unit(u'm/s⁴',   _(u'm/s⁴'),     _(u'm/s⁴'),     1),
]

UNITS_CRACKLE = [
    Unit(u'm/s⁵',   _(u'm/s⁵'),     _(u'm/s⁵'),     1),
]

UNITS_INERTIA_TORQUE = [
    Unit(u'kgm²',   _(u'kgm²'),     _(u'kgm²'),     1 ),
    Unit(u'kgcm²',  _(u'kgcm²'),    _(u'kgcm²'),    0.0001 ),
    Unit(u'kgmm²',  _(u'kgmm²'),    _(u'kgmm²'),    0.000001 ),
]

UNITS_TORSION = [
    Unit(u'Nm/arcmin',  _(u'Nm/arcmin'),    _(u'Nm/arcmin'),    1),
]

UNITS_ANGLE_VELOCITY = [
    Unit(u'rad/s',    _(u'rad/s'),    _(u'Radians/s'),  1 ),
    Unit(u'deg/s',    _(u'°/s'),      _(u'Degrees/s'),  math.pi / 180 ),
    Unit(u'rps',      _(u'rps'),      _(u'rps'), (math.pi * 2.0)),
    Unit(u'rpm',      _(u'rpm'),      _(u'rpm'), (math.pi * 2.0) / 60.0),
]

UNITS_ANGLE_ACCELERATION = [
    Unit(u'rad/s²',    _(u'rad/s²'),    _(u'Radians/s²'),  1 ),
    Unit(u'deg/s²',    _(u'°/s²'),      _(u'Degrees/s²'),  math.pi / 180 ),
    Unit(u'rps²',      _(u'rps²'),      _(u'rps²'), 1.0 / (math.pi * 2.0)),
    Unit(u'rpm²',      _(u'rpm²'),      _(u'rps²'), (math.pi * 2.0) / 3600.0),
]

UNITS_ANGLE_JERK = [
    Unit(u'rad/s³',    _(u'rad/s³'),    _(u'Radians/s³'),  1 ),
    Unit(u'deg/s³',    _(u'°/s³'),      _(u'Degrees/s³'),  math.pi / 180 ),
    Unit(u'rps³',      _(u'rps³'),      _(u'rps³'), 1.0 / (math.pi * 2.0)),
    Unit(u'rpm³',      _(u'rpm³'),      _(u'rpm³'),
        (math.pi * 2.0) / (60.0 * 60.0 * 60.0)),
]
    #Unit(u'grad/s³',   _(u'grad/s³'),   _(u'Grads/s³'),    math.pi / 200 ),

UNITS_ANGLE_SNAP = [
    Unit(u'rad/s⁴',    _(u'rad/s⁴'),    _(u'Radians/s⁴'),  1 ),
    Unit(u'deg/s⁴',    _(u'°/s⁴'),      _(u'Degrees/s⁴'),  math.pi / 180 ),
    #Unit(u'grad/s⁴',   _(u'grad/s⁴'),   _(u'Grads/s⁴'),    math.pi / 200 ),
    Unit(u'rps⁴',      _(u'rps⁴'),      _(u'rps⁴'), 1.0 / (math.pi * 2.0)),
    Unit(u'rpm⁴',      _(u'rpm⁴'),      _(u'rpm⁴'),
        (math.pi * 2.0) / (60.0 * 60.0 * 60.0 * 60.0)),
]

UNITS_ANGLE_CRACKLE = [
    Unit(u'rad/s⁵',    _(u'rad/s⁵'),    _(u'Radians/s⁵'),  1 ),
    Unit(u'deg/s⁵',    _(u'°/s⁵'),      _(u'Degrees/s⁵'),  math.pi / 180 ),
    #Unit(u'grad/s⁵',   _(u'grad/s⁵'),   _(u'Grads/s⁵'),    math.pi / 200 ),
    Unit(u'rps⁵',      _(u'rps⁵'),      _(u'rps⁵'), 1.0 / (math.pi * 2.0)),
    Unit(u'rpm⁵',      _(u'rpm⁵'),      _(u'rpm⁵'),
        (math.pi * 2.0) / (60.0 * 60.0 * 60.0 * 60.0 * 60.0)),
]


# Electric Units

UNITS_POWER = [
    Unit(u'W',   _(u'W'),     _(u'watt'),     1),
]

# Wärmewiderstand
UNITS_THERMAL_RESISTANCE = [
    Unit(u'K/W',   _(u'K/W'),     _(u'K/W'),     1),
]

# Wärmedurchgangswiderstand
UNITS_HEAT_TRANSFER_RESISTANCE = [
    Unit(u'w/(m²K)',   _(u'w/(m²K)'),     _(u'W/(m²K)'),     1),
]

# Wärmeleitfähigkeit
UNITS_HEAT_CONDUCTANCE = [
    Unit(u'W/(mK)',   _(u'W/(mK)'),     _(u'W/(mK)'),     1),
]

UNITS_HEAT_CAPACITY = [
    Unit(u'Ws/K',   _(u'Ws/K'),     _(u'Ws/K'),     1),
]

UNITS_SPECIFIC_HEAT_CAPACITY = [
    Unit(u'Ws/(kgK)',   _(u'Ws/(kgK)'),     _(u'Ws/(kgK)'),     1),
]

UNITS_MOTOR_CONSTANT = [
    Unit(u'Nm/W^(1/2)',   _(u'Nm/W^(1/2)'),     _(u'Nm/W^(1/2)'),     1),
]

UNITS_FORCE_CONSTANT = [
    Unit(u'N/A',   _(u'N/A'),     _(u'N/A'),     1),
]

UNITS_POTENTIAL_CONSTANT = [
    Unit(u'Vs/m',   _(u'Vs/m'),     _(u'Vs/m'),     1),
]

UNITS_ELECTRICAL_TIME_CONSTANT = [
    Unit(u'ms',   _(u'ms'),     _(u'ms'),     1),
]

UNITS_ELECTRICAL_RESISTANCE = [
    Unit(u'Ω',   _(u'Ω'),     _(u'ohm'),     1),
]

UNITS_INDUCTANCE = [
    Unit(u'mH',   _(u'mH'),     _(u'mH'),     1),
]

UNITS_FLOW_RATE = [
    Unit(u'm³/h',   _(u'm³/h'),     _(u'm³/h'),     1),
]

UNITS_FLOW_RATE_CHOICES = get_choices(UNITS_FLOW_RATE)
UNITS_THERMAL_RESISTANCE_CHOICES = get_choices(UNITS_THERMAL_RESISTANCE)
UNITS_MOTOR_CONSTANT_CHOICES = get_choices(UNITS_MOTOR_CONSTANT)
UNITS_FORCE_CONSTANT_CHOICES = get_choices(UNITS_FORCE_CONSTANT)
UNITS_POTENTIAL_CONSTANT_CHOICES = get_choices(UNITS_POTENTIAL_CONSTANT)
UNITS_ELECTRICAL_TIME_CONSTANT_CHOICES = get_choices(
    UNITS_ELECTRICAL_TIME_CONSTANT)
UNITS_ELECTRICAL_RESISTANCE_CHOICES = get_choices(UNITS_ELECTRICAL_RESISTANCE)
UNITS_INDUCTANCE_CHOICES = get_choices(UNITS_INDUCTANCE)

UNITS_ACCELERATION_CHOICES = get_choices(UNITS_ACCELERATION)
UNITS_ANGLE_CHOICES = get_choices(UNITS_ANGLE)
UNITS_CRACKLE_CHOICES = get_choices(UNITS_CRACKLE)
UNITS_CURRENT_CHOICES = get_choices(UNITS_CURRENT)
UNITS_DENSITY_CHOICES = get_choices(UNITS_DENSITY)
UNITS_FORCE_CHOICES = get_choices(UNITS_FORCE)
UNITS_INERTIA_TORQUE_CHOICES = get_choices(
    UNITS_INERTIA_TORQUE)
UNITS_JERK_CHOICES = get_choices(UNITS_JERK)
UNITS_POTENTIAL_CHOICES = get_choices(UNITS_POTENTIAL)
UNITS_POWER_CHOICES = get_choices(UNITS_POWER)
UNITS_SNAP_CHOICES = get_choices(UNITS_SNAP)
UNITS_SPEED_CHOICES = get_choices(UNITS_SPEED)
UNITS_TORQUE_CHOICES = get_choices(UNITS_TORQUE)
UNITS_VELOCITY_CHOICES = get_choices(UNITS_VELOCITY)
UNITS_TORSION_CHOICES = get_choices(UNITS_TORSION)

UNITS_ANGLE_VELOCITY_CHOICES = get_choices(UNITS_ANGLE_VELOCITY)
UNITS_ANGLE_ACCELERATION_CHOICES = get_choices(UNITS_ANGLE_ACCELERATION)
UNITS_ANGLE_JERK_CHOICES = get_choices(UNITS_ANGLE_JERK)
UNITS_ANGLE_SNAP_CHOICES = get_choices(UNITS_ANGLE_SNAP)
UNITS_ANGLE_CRACKLE_CHOICES = get_choices(UNITS_ANGLE_CRACKLE)
