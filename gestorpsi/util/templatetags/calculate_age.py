from django import template
import datetime

register = template.Library()

def age(bday, d=None):
    """ http://www.djangosnippets.org/snippets/557/ """
    if d is None:
        d = datetime.date.today()
    return (d.year - bday.year) - int((d.month, d.day) < (bday.month, bday.day))

register.filter('age', age)

