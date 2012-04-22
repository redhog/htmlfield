# -*- coding: utf-8 -*-

# Copyright 2011-2012 Egil Möller
# License: LGPL 3

# A simple unintrusive django db field for html content, with wysiwyg
# editing in django admin that does not take over all of the admin or
# makes all other fields wysiwyg editable.

# Use like any TextField in your models, but pass through the safe
# filter in templates like this: {{ somemodel.somefield|safe }}


from django.utils.translation import ugettext_lazy as _
import django.forms
from django.utils.safestring import mark_safe
from django.forms.util import flatatt
from django.utils.html import escape, conditional_escape
import django.db.models
from django.utils.encoding import StrAndUnicode, force_unicode, smart_unicode
from django.conf import settings

class HtmlTextarea(django.forms.Textarea):
    class Media:
         js = (settings.STATIC_URL + '/ckeditor/ckeditor.js',)
    def render(self, name, value, attrs=None):
        if value is None: value = ''
        if not attrs: attrs = {}
        if 'class' not in attrs: attrs['class'] = ''
        attrs['class'] += ' ckeditor'
        final_attrs = self.build_attrs(attrs, name=name)
        return mark_safe(u'<textarea%s>%s</textarea>' % (flatatt(final_attrs),
                conditional_escape(force_unicode(value))))

class HtmlField(django.db.models.Field):
    description = _("Html")

    def db_type(self, connection):
        return 'text'

    def get_internal_type(self):
        return "HtmlField"

    def get_prep_value(self, value):
        if isinstance(value, basestring) or value is None:
            return value
        return smart_unicode(value)

    def formfield(self, **kwargs):
        defaults = {'widget': HtmlTextarea}
        defaults.update(kwargs)
        return super(HtmlField, self).formfield(**defaults)
