import json

import requests
from django.shortcuts import render

# Create your views here.
def index(req):
    return render(req, "index.html", {})

def build(req):
    items = json.loads(req.POST["items"])
    #print(items)
    return render(req, "build.html", {"items": items})

