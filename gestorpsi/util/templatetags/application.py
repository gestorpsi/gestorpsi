from django.contrib.sites.models import Site
from django.contrib.sites.models import RequestSite
from django import template
register = template.Library()

@register.simple_tag
def capturing_protocol_domain(request):
    site_info = {'protocol': request.is_secure() and 'https' or 'http'}
    if Site._meta.installed:
        site_info['domain'] = Site.objects.get_current().domain
    else:
        site_info['domain'] = RequestSite(request).domain
    return site_info