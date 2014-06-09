# -*- coding: utf-8 -*-
from unit_field.fields import get_factor
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def get_normalized_value(value, unit, units):
    factor = get_factor(units, unit)
    if factor is None:
        raise ValidationError(_(u'The selected unit could not be found'))
    return value * factor

def validate_lte(input_value, input_unit, limit_value, limit_unit, units):
    normalized_value = get_normalized_value(input_value, input_unit, units)
    normalized_limit = get_normalized_value(limit_value, limit_unit, units)

    if normalized_value > normalized_limit:
        raise ValidationError(
            _(u'%(input_value)s %(input_unit)s has to be lower than ' \
                u'or equal %(limit_value)s %(limit_unit)s') % {
                    'input_value': input_value,
                    'input_unit': input_unit,
                    'limit_value': limit_value,
                    'limit_unit': limit_unit,
                })

def validate_lt(input_value, input_unit, limit_value, limit_unit, units):
    normalized_value = get_normalized_value(input_value, input_unit, units)
    normalized_limit = get_normalized_value(limit_value, limit_unit, units)

    if normalized_value >= normalized_limit:
        raise ValidationError(
            _(u'%(input_value)s %(input_unit)s has to be lower than ' \
                u'%(limit_value)s %(limit_unit)s') % {
                    'input_value': input_value,
                    'input_unit': input_unit,
                    'limit_value': limit_value,
                    'limit_unit': limit_unit,
                })

def validate_gte(input_value, input_unit, limit_value, limit_unit, units):
    normalized_value = get_normalized_value(input_value, input_unit, units)
    normalized_limit = get_normalized_value(limit_value, limit_unit, units)

    if normalized_value < normalized_limit:
        raise ValidationError(
            _(u'%(input_value)s %(input_unit)s has to be greater than ' \
                u'or equal %(limit_value)s %(limit_unit)s') % {
                    'input_value': input_value,
                    'input_unit': input_unit,
                    'limit_value': limit_value,
                    'limit_unit': limit_unit,
                })

def validate_gt(input_value, input_unit, limit_value, limit_unit, units):
    normalized_value = get_normalized_value(input_value, input_unit, units)
    normalized_limit = get_normalized_value(limit_value, limit_unit, units)

    if normalized_value <= normalized_limit:
        raise ValidationError(
            _(u'%(input_value)s %(input_unit)s has to be greater than ' \
                u'%(limit_value)s %(limit_unit)s') % {
                    'input_value': input_value,
                    'input_unit': input_unit,
                    'limit_value': limit_value,
                    'limit_unit': limit_unit,
                })
