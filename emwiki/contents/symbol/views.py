from django.shortcuts import render
from django.http.response import JsonResponse
import os
import urllib
from contents.symbol.models import Symbol
from emwiki.settings import STATIC_SYMBOLS_URL
