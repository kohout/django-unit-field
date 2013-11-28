# -*- coding: utf-8 -*-
from django.db.models import FloatField, CharField as ModelCharField
from django.forms import CharField
from unit_field.units import (Unit, UnitValueCreator,
    UNITS_LENGTH,
    UNITS_SQUARE_MEASURE,
    UNITS_SOLID_MEASURE,
    UNITS_MASS,
    UNITS_TIME,
    UNITS_ELECTRIC_CURRENT,
    UNITS_TEMPERATURE,
    UNITS_AMOUNT_OF_SUBSTANCE,
    UNITS_LUMINOUS_INTENSITY,

    UNITS_ACCELERATION,
    UNITS_ANGLE,
    UNITS_CRACKLE,
    UNITS_CURRENT,
    UNITS_DENSITY,
    UNITS_FORCE,
    UNITS_INERTIA_TORQUE,
    UNITS_JERK,
    UNITS_POTENTIAL,
    UNITS_SNAP,
    UNITS_SPEED,
    UNITS_TORSION,
    UNITS_TORQUE,
    UNITS_VELOCITY,

    UNITS_POWER,
    UNITS_THERMAL_RESISTANCE,
    UNITS_MOTOR_CONSTANT,
    UNITS_FORCE_CONSTANT,
    UNITS_ELECTRICAL_TIME_CONSTANT,
    UNITS_POTENTIAL_CONSTANT,
    UNITS_ELECTRICAL_RESISTANCE,
    UNITS_INDUCTANCE)


from unit_field import forms

try:
    from hashlib import md5
except ImportError:
    from md5 import new as md5

def md5_hexdigest(value):
    return md5(value).hexdigest()

def get_factor(units, unit_id):
    """
    Returns the factor of a Unit-Config
    """
    if not units:
        return None

    for unit in units:
        if unit.id == unit_id:
            return unit.factor

class UnitInputField(FloatField):

    auto_convert = True

    def __init__(self, *args, **kwargs):
        auto_convert = kwargs.pop('auto_convert', None)
        if auto_convert is not None:
            self.auto_convert = auto_convert
        super(UnitInputField, self).__init__(*args, **kwargs)

    def get_prep_value(self, value):
        try:
            return float(value)
        except TypeError, ValueError:
            return 0.0

    def formfield(self, **kwargs):
        if self.auto_convert:
            defaults = {'form_class': forms.UnitInputField }
        else:
            defaults = {'form_class': CharField }
        defaults.update(kwargs)
        return super(UnitInputField, self).formfield(**defaults)

class CalculatedFloatField(FloatField):
    """
    This field is required to define the special behaviour of the
    pre-calculated field, used in UnitField
    """
    units = None

    def get_unit_by_id(self, unit_id):
        """
        returns the unit factor of the desired unit, e.g.:
        get_unit_by_id(u'dm²') ---> 0.01
        """
        return get_factor(self.units, unit_id)

    def __init__(self, *args, **kwargs):
        kwargs['editable'] = False
        self.units = kwargs.pop('units', None)
        super(CalculatedFloatField, self).__init__(*args, **kwargs)
        self.default = 0.0

    def pre_save(self, model_instance, add):
        input_field_name = self.attname.replace('_value', '_input')
        unit_field_name = self.attname.replace('_value', '_unit')

        input_value = getattr(model_instance, input_field_name)
        unit_id = getattr(model_instance, unit_field_name)

        unit_value = self.get_unit_by_id(unit_id)

        if (input_value is not None) and (unit_value is not None):
            setattr(model_instance, self.attname, input_value * unit_value)
        else:
            setattr(model_instance, self.attname, 0.0)

        return getattr(model_instance, self.attname)

class UnitField(FloatField):
    """
    a compound field contributes three columns to the model instead of the
    standard single column
    """
    choices = None

    units = []

    auto_convert = True

    verbose_name = u'(UnitField)'

    blank = False

    null = False

    default_unit = None

    validators = []

    def update_choices(self):
        """
        generates choices list, if not set
        """
        if self.choices is None:
            self.choices = []
            for unit in self.units:
                self.choices.append((unit.id, unit.abbrev, ))

    def get_base_unit(self):
        """
        returns the unit with factor == 1.0
        """
        if self.units:
            for unit in self.units:
                if unit.factor == 1.0:
                    return unit
        return None

    def get_base_unit_id(self):
        """
        returns the identifier of the base unit (e.g. "m²")
        """
        base_unit = self.get_base_unit()
        if base_unit is None:
            return None

        return base_unit.id

    def __init__(self, *args, **kwargs):
        if 'choices' in kwargs:
            raise TypeError("%s invalid attribute 'choices'" % (
                self.__class__.__name__, ))
        self.auto_convert = kwargs.pop('auto_convert', True)
        self.verbose_name = kwargs.get('verbose_name')
        self.blank = kwargs.get('blank')
        self.null = kwargs.get('null')
        self.validators = kwargs.get('validators', [])
        kwargs['editable'] = False
        kwargs['default'] = 0.

        self.default_unit = kwargs.pop('default_unit',
            self.get_base_unit_id())
        self.update_choices()
        super(UnitField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        self.name = name

        self.input_field = UnitInputField(default=0,
            blank=self.blank,
            null=self.null,
            auto_convert=self.auto_convert,
            validators=self.validators,
            verbose_name=self.verbose_name)
        cls.add_to_class("%s_input" % (self.name,), self.input_field)

        # self.unit_field = CharField(default=self.default_unit, choices=self.choices)
        self.unit_field = ModelCharField(max_length=10,
            default=self.default_unit,
            choices=self.choices)
        cls.add_to_class("%s_unit" % (self.name,), self.unit_field)

        self.value_field = CalculatedFloatField(default=0.0,
            units=self.units,
            blank=self.blank,
            null=self.null)
        cls.add_to_class("%s_value" % (self.name,), self.value_field)

        self.key = md5_hexdigest(self.name)

        field = UnitValueCreator(self)

        setattr(cls, name, field)

    def get_db_prep_save(self, value):
        pass

    def get_db_prep_lookup(self, lookup_type, value):
        raise NotImplementedError(self.get_db_prep_lookup)

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.UnitField}
        defaults.update(kwargs)
        return super(UnitField, self).formfield(**defaults)

# Fields for Base Units

class LengthField(UnitField):
    units = UNITS_LENGTH

class SquareMeasureField(UnitField):
    units = UNITS_SQUARE_MEASURE

class SolidMeasureField(UnitField):
    units = UNITS_SOLID_MEASURE

class MassField(UnitField):
    units = UNITS_MASS

class TimeField(UnitField):
    units = UNITS_TIME

class TemperatureField(UnitField):
    units = UNITS_TEMPERATURE

class AmountOfSubstanceField(UnitField):
    units = UNITS_AMOUNT_OF_SUBSTANCE

class LuminousIntensityField(UnitField):
    units = UNITS_LUMINOUS_INTENSITY

# Fields for Derived Units

class AccelerationField(UnitField):
    units = UNITS_ACCELERATION

class AngleField(UnitField):
    units = UNITS_ANGLE

class CrackleField(UnitField):
    units = UNITS_CRACKLE

class CurrentField(UnitField):
    units = UNITS_CURRENT

class DensityField(UnitField):
    units = UNITS_DENSITY

class ForceField(UnitField):
    units = UNITS_FORCE

class InertiaTorqueField(UnitField):
    units = UNITS_INERTIA_TORQUE

class JerkField(UnitField):
    units = UNITS_JERK

class PotentialField(UnitField):
    units = UNITS_POTENTIAL

class SnapField(UnitField):
    units = UNITS_SNAP

class SpeedField(UnitField):
    units = UNITS_SPEED

class TorqueField(UnitField):
    units = UNITS_TORQUE

class VelocityField(UnitField):
    units = UNITS_VELOCITY

class TorsionField(UnitField):
    units = UNITS_TORSION

class PowerField(UnitField):
    units = UNITS_POWER

class ThermalResistanceField(UnitField):
    units = UNITS_THERMAL_RESISTANCE

class ElectricalTimeConstantField(UnitField):
    units = UNITS_ELECTRICAL_TIME_CONSTANT

class MotorConstantField(UnitField):
    units = UNITS_MOTOR_CONSTANT

class ForceConstantField(UnitField):
    units = UNITS_FORCE_CONSTANT

class PotentialConstantField(UnitField):
    units = UNITS_POTENTIAL_CONSTANT

class ResistanceField(UnitField):
    units = UNITS_ELECTRICAL_RESISTANCE

class InductanceField(UnitField):
    units = UNITS_INDUCTANCE

try:
    from south.modelsinspector import add_introspection_rules
    rules = [((CalculatedFloatField, ), [], {}),]
    add_introspection_rules(rules, [
        "^unit_field\.fields"])
except ImportError:
    pass
