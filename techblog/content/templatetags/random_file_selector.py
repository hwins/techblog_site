from django import template
from random import Random

register = template.Library()


@register.simple_tag
def random_file_number():
    rand = Random()
    tens = rand.randint(0, 2)
    ones = rand.randint(0, 9)
    return str(tens) + str(ones)
