from django import template
from ..models import Sanction

register = template.Library()

@register.filter
def sanction_badge_class(statut):
    """
    Retourne la classe CSS appropriée pour le badge de statut d'une sanction
    """
    badge_classes = {
        'en_attente': 'badge-warning',
        'appliquee': 'badge-success',
        'annulee': 'badge-danger',
        'contestee': 'badge-info'
    }
    return badge_classes.get(statut, 'badge-secondary') 