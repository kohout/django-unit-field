# -*- coding: utf-8 -*-
from django.db.models import FloatField
from django.forms import CharField
from unit_field.units import (Unit, UnitValueCreator,
    UNITS_LENGTH_CHOICES,
    UNITS_SQUARE_MEASURE_CHOICES,
    UNITS_SOLID_MEASURE_CHOICES,
    UNITS_MASS_CHOICES,
    UNITS_TIME_CHOICES,
    UNITS_ELECTRIC_CURRENT_CHOICES,
    UNITS_TEMPERATURE_CHOICES,
    UNITS_AMOUNT_OF_SUBSTANCE_CHOICES,
    UNITS_LUMINOUS_INTENSITY_CHOICES)
from unit_field import forms

try:
    from hashlib import md5
except ImportError:
    from md5 import new as md5

def md5_hexdigest(value):
    return md5(value).hexdigest()

class UnitInputField(FloatField):

    auto_convert = True

    def __init__(self, *args, **kwargs):
        auto_convert = kwargs.pop('auto_convert', None)
        if auto_convert is not None:
            self.auto_convert = auto_convert
        super(UnitInputField, self).__init__(*args, **kwargs)

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

    def __init__(self, *args, **kwargs):
        kwargs['editable'] = False
        super(CalculatedFloatField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        input_field_name = self.attname.replace('_value', '_input')
        unit_field_name = self.attname.replace('_value', '_unit')

        input_value = getattr(model_instance, input_field_name)
        unit_value = getattr(model_instance, unit_field_name)

        setattr(model_instance, self.attname, input_value * unit_value)
        return getattr(model_instance, self.attname)

class UnitField(FloatField):
    """
    a compound field contributes three columns to the model instead of the
    standard single column
    """
    choices = [ (1, '?',) ]

    auto_convert = True

    def __init__(self, *args, **kwargs):
        if 'choices' in kwargs:
            raise TypeError("%s invalid attribute 'choices'" % (
                self.__class__.__name__, ))
        self.units = kwargs.pop('units', [])
        self.auto_convert = kwargs.pop('auto_convert', True)
        kwargs['editable'] = False
        kwargs['default'] = 0.
        super(UnitField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        self.name = name

        self.input_field = UnitInputField(default=0, blank=True,
            auto_convert=self.auto_convert)
        cls.add_to_class("%s_input" % (self.name,), self.input_field)

        self.unit_field = FloatField(default=1, choices=self.choices)
        cls.add_to_class("%s_unit" % (self.name,), self.unit_field)

        self.value_field = CalculatedFloatField()
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


class LengthField(UnitField):
    choices = UNITS_LENGTH_CHOICES

class SquareMeasureField(UnitField):
    choices = UNITS_SQUARE_MEASURE_CHOICES

class SolidMeasureField(UnitField):
    choices = UNITS_SOLID_MEASURE_CHOICES

class MassField(UnitField):
    choices = UNITS_MASS_CHOICES

class TimeField(UnitField):
    choices = UNITS_TIME_CHOICES

class TemperatureField(UnitField):
    choices = UNITS_TEMPERATURE_CHOICES

class AmountOfSubstanceField(UnitField):
    choices = UNITS_AMOUNT_OF_SUBSTANCE_CHOICES

class LuminousIntensityField(UnitField):
    choices = UNITS_LUMINOUS_INTENSITY_CHOICES
