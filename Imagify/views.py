from django.http import HttpResponse
# from django.template.loader import render_to_string
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    context={}
    # HTML_STRING=render_to_string("home-view.html",context)
    # return HttpResponse(HTML_STRING)
    return render(request,"home-view.html",context)