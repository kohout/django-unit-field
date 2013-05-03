#################
django-unit-field
#################

a new field inherited from FloatField with a custom widget that allows unit conversion.

============
Installation
============

You will need to add ``unit_field`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        # ...
        'unit_field',
    )

========
Abstract
========

django-unit-field provides a set of Fields for your model. Each field will create three columns in the corresponding database that holds all required informations. These classes are located in ``unit_field.fields``::

 * LengthField (base unit: m=1)
 * SquareMeasureField (base unit: m²=1)
 * SolidMeasureField (base unit: m³=1)
 * MassField (base unit: g=1)
 * TimeField (base unit: s=1)
 * TemperatureField (base unit: K=1)
 * AmountOfSubstanceField (base unit: mol=1)
 * LuminousIntensityField (base unit: cd=1)

===================
Enhance your models
===================

Example::

    from unit_field.fields import SolidMeasureField, TemperatureField

    class Engine(models.Model):
        cubic_capacity = SolidMeasureField(
            verbose_name=u'cubic capacity')
        operating_temperature = TemperatureField(
            verbose_name=u'operatiing temperature')

==================================
Enable client-side unit conversion
==================================

If you want to use client-side unit conversion, you have to include the static javascript file located in the ``static`` directory of the app::

    <script src="http://ajax.googleapis.com/ajax/libs/jquery/{{jquery-version}}/jquery.min.js"></script>
    <script src="{{ STATIC_URL }}js/jquery.unit-field.js"></script>

If you want to exclude some fields from automatic conversion, you can use the additional parameter ``auto_convert``::

    class Engine(models.Model):
        ...
        operating_temperature = TemperatureField(auto_convert=False,
            verbose_name=u'operatiing temperature')

====================
Declare custom units
====================

TODO: Describe how to inherit from class ``UnitField``.
