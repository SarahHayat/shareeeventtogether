from django.urls import reverse_lazy, reverse
from django.utils.translation import ugettext_lazy as _

from persons.models import Person

NAV_HOME = 'Home'
NAV_EVENEMENT = 'Evenement'

SHORTCUT_HOME = 'home'
SHORTCUT_EVENEMENT = 'details'

NAV_ITEMS = (
    (NAV_HOME, SHORTCUT_HOME),
    (NAV_EVENEMENT, SHORTCUT_EVENEMENT),
)


def navigation_items(selected_item=None):
    items = []
    for name, shortcut in NAV_ITEMS:
        items.append({
            'name': name,
            'url': reverse(shortcut),
            'active': True if selected_item == name else False,
        })
    return items
