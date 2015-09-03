from django.contrib.sites.models import Site
from django import template
register = template.Library()


@register.simple_tag
def hostname():
    return Site.objects.get_current().domain
    
