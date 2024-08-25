
menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Обратная связь", 'url_name': 'contact'},
]


def get_site_context(request):
    return {'mainmenu': menu, 'index_ignore_list': ['about', 'contact']}