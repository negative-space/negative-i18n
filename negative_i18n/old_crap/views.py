import json
import os
from shutil import copyfileobj

from negative_i18n.models import StringTranslation
from django.conf import settings
from django.http import HttpResponse, Http404
from django.middleware.csrf import get_token
from django.template import Context
from django.template import Template


def send_file(response, name):
    path = os.path.join(settings.APP.get(I18n).get_dir(), 'ui-app', name)
    with open(path) as f:
        copyfileobj(f, response)

    response.write("\n\n")


def send_file_template(response, name, context):
    path = os.path.join(settings.APP.get(I18n).get_dir(), 'templates', name)
    with open(path) as f:
        template = Template(f.read())
        context = Context(context)
        response.write(template.render(context))


def trans_js(request):
    response = HttpResponse(content_type="application/javascript; charset=utf-8")

    response['csrftoken'] = get_token(request)

    data_ = StringTranslationSerializer(StringTranslation.objects.all(), many=True).data

    send_file_template(response, 'trans.js', {'data': json.dumps(data_, ensure_ascii=False, indent=4).encode('utf8')})

    return response
