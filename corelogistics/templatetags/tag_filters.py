import re
from django.utils.html import mark_safe
from django import template
from django.contrib.auth.models import Group

register = template.Library()

#for form styling with bootstrap
#Source: http://stackoverflow.com/a/4124698
class_re = re.compile(r'(?<=class=["\'])(.*)(?=["\'])')
@register.filter
def add_class(value, css_class):
    match = class_re.search(value)
    if match:
        m = re.search(r'^%s$|^%s\s|\s%s\s|\s%s$' % (css_class, css_class,
                                                    css_class, css_class),
                                                    match.group(1))
        print(match.group(1))
        if not m:
            return mark_safe(class_re.sub(match.group(1) + " " + css_class,
                                          value))
    else:
        return mark_safe(value.replace('>', ' class="%s">' % css_class))
    return value


#Source: http://stackoverflow.com/questions/34571880/how-to-check-in-template-whether-user-belongs-to-group
@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return group in user.groups.all()
