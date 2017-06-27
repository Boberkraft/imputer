from flask_babel import gettext as _

ALLOWED_MODE = ('selected', 'database')
ALLOWED_ACTION = ('add', 'select', 'delete', 'unselect')

LANGUAGES = {
    'en': 'English',
    'pl': 'Polish'
}
navigation_tabs = [('/', _('Menu')),
                   ('/add/', _('Add')),
                   ('/upload/', _('Search')),
                   ('/update/', _('About'))]

images_path = '/uploads/'

