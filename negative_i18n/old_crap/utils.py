from django.conf import settings
from slugify import slugify


def localize_slug(target_field, slug_field='slug'):
    class LocalizedSlugGeneratorMixin(object):

        def save(self, *args, **kwargs):

            for lang, name in settings.LANGUAGES:
                if not getattr(self, '{}_{}'.format(slug_field, lang)) and getattr(self, '{}_{}'.format(target_field, lang)):
                    setattr(self, '{}_{}'.format(slug_field, lang), slugify(getattr(self, '{}_{}'.format(target_field, lang)), to_lower=True))

            super().save(*args, **kwargs)

    return LocalizedSlugGeneratorMixin
