# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe

class UnitModelMixin(object):

    def __getattr__(self, name):
        if name.endswith('_html'):
            _field = name.replace('_html', '_input')
            _label = self._meta.get_field(_field).verbose_name

            _unit_field = name.replace('_html', '_unit')
            _val = getattr(self, _field)
            _method_name = u'get_%s_display' % _unit_field
            _unit_method = getattr(self, _method_name)
            return mark_safe(u'<div class="row-fluid">' \
                '<div class="span6">%s:</div>' \
                '<div class="span6"><strong>%s %s</strong></div>' \
                '</div>' % (
                _label, _val, _unit_method(), ))

        if name.endswith('_label_key'):
            _field = name.replace('_label_key', '_input')
            return self._meta.get_field(_field).verbose_name

        if name.endswith('_label_value'):
            _field = name.replace('_label_value', '_input')
            _unit_field = name.replace('_label_value', '_unit')
            _val = getattr(self, _field)
            _method_name = u'get_%s_display' % _unit_field
            _unit_method = getattr(self, _method_name)
            return u'%s %s' % (_val, _unit_method(), )

        return super(UnitModelMixin, self).__getattr__(name)
