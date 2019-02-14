from django.conf import settings

from django.utils.translation import get_language


def i18n_context(request):
    """
    @type context: HttpRequest
    """

    context = {
        'lang': get_language(),
        'default_lang': settings.LANGUAGE_CODE,
        'lang_name': dict(settings.LANGUAGES)[get_language()],
        'langs': settings.LANGUAGES
    }

    return context