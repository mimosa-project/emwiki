from django.apps import AppConfig

from emwiki.settings import CONTENTS_DIR


class ContentsConfig(AppConfig):
    name = 'contents.contents'
    path = CONTENTS_DIR
