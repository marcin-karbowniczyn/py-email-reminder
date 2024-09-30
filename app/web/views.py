from django.shortcuts import render


# Placeholder view
def index(req):
    return render(req, 'index.html')
