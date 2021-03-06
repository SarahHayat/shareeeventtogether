from django.urls import reverse

NAV_EVENEMENT = 'Évenement'
NAV_HOME = 'Accueil'

SHORTCUT_EVENEMENT = 'events'
SHORTCUT_HOME = 'home'

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
