# coding: utf-8
import os
import sys
from collections import OrderedDict

from cratis.features import Feature, require
from cratis_admin.features import AdminArea
from cratis_api.features import RestApi


#
# orig_gettext = translation.gettext
#
# def new_gettext(message):
#     print('New trans: {}'.format(message))
#     return orig_gettext(message)
#
# translation.gettext = new_gettext
#
# orig_gettext = translation.gettext
#
# def new_gettext(message):
#     print('New trans: {}'.format(message))
#     return orig_gettext(message)
#
# translation.gettext = new_gettext

# from django.utils.translation import gettext as _
from cratis_common.threadlocal import ThreadLocalRequest


@require(
    RestApi(),
    ThreadLocalRequest()
)
class I18n(Feature):

    def __init__(self,
                 langs=('en',),
                 main_lang='en',
                 lang_urls=None,
                 translation_base_lang=None,
                 admin_lang=None,
                 collect_stats=False,
                 fallback_translations=False,
                 django_url_middleware=False
                 ):
        super().__init__()

        self.main_lang = main_lang
        self.collect_stats = collect_stats
        self.translation_base_lang = translation_base_lang or main_lang
        self.admin_lang = admin_lang or main_lang
        self.lang_urls = lang_urls
        self.django_url_middleware = django_url_middleware

        from django.conf.locale import LANG_INFO

        _langs = OrderedDict()
        for code in langs:
            name = LANG_INFO[code]['name_local'].capitalize()
            _langs[code] = name

        if len(_langs) == 0:
            _langs = {'en': 'English'}

        self.langs = tuple([(code, name) for code, name in _langs.items()])

        self.fallback_translations = fallback_translations

    def get_deps(self):
        return [
            'django-modeltranslation', 'solid_i18n', 'polib'
        ]

    def configure_settings(self):

        self.append_apps([
                'negative_i18n',
            ])

        # disable i18n when generating migrations

        if 'makemigrations' not in sys.argv:
            self.append_apps([
                'modeltranslation',
            ])

        cls = self.settings

        cls.USE_FALLBACK_TRANSLATION = self.fallback_translations
        cls.MODELTRANSLATION_FALLBACK_LANGUAGES = tuple(dict(self.langs).keys())

        cls.COLLECT_I18N_STATS = self.collect_stats
        cls.LANGUAGE_CODE = self.main_lang
        cls.TRANSLATION_BASE_LANG = getattr(cls, 'TRANSLATION_BASE_LANG', self.translation_base_lang)
        cls.USE_I18N = True
        cls.USE_L10N = True
        cls.LANG_URLS = self.lang_urls

        if self.langs:
            cls.LANGUAGES = self.langs

        cls.MAIN_LANGUAGE = self.main_lang
        cls.ADMIN_LANGUAGE = self.admin_lang

        self.append_template_dir(os.path.dirname(__file__) + '/templates')

        self.append_template_processor(
            ('negative_i18n.context.i18n_context', 'django.template.context_processors.request',)
        )

        cls.USE_FALLBACK_TRANSLATION = self.fallback_translations

        if self.django_url_middleware:
            self.append_middleware(
                'django.middleware.locale.LocaleMiddleware'
            )

        with self.use(RestApi) as api:
            api.routes.append(
                (r'i18n', 'negative_i18n.views.StringTranslationViewSet')
            )

        self.append_template_builtins('negative_i18n.templatetags.translate')

    def configure_urls(self, urls):
        from .views import trans_js
        from django.conf.urls import url

        urls += (
            url(r'^api/trans-data$', trans_js, name='trans_api'),
        )


@require(
    AdminArea()
)
class I18nAdmin(Feature):
    def init(self):

        with self.use(AdminArea) as admin:
            admin.assets.require_css('modeltranslation/css/tabbed_translation_fields.css')
            admin.assets.require_js(
                'modeltranslation/js/jquery-ui.min.js',
                'modeltranslation/js/tabbed_translation_fields.js'
            )