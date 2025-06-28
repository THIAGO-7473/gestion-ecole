from django import template

register = template.Library()

@register.filter
def get_periode_display(value):
    periodes = {
        'premier': 'Première Période',
        'second': 'Seconde Période',
        'troisieme': 'Troisième Période',
        'quatrieme': 'Quatrième Période'
    }
    return periodes.get(value, value) 