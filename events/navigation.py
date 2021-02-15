from django.urls import  reverse


NAV_EVENEMENT = 'Evenement'
NAV_PROFIL = 'Profil'
NAV_HOME = 'Home'

SHORTCUT_EVENEMENT = 'events'
SHORTCUT_PROFIL = 'profil'
SHORTCUT_HOME = 'home'

NAV_ITEMS = (
    (NAV_HOME, SHORTCUT_HOME),
    (NAV_EVENEMENT, SHORTCUT_EVENEMENT),
    (NAV_PROFIL, SHORTCUT_PROFIL),
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
