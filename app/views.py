from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, "index.html", {"days": ["monday", 
                                                   "tuesday", 
                                                   "wednesday", 
                                                   "thursday", 
                                                   "friday", 
                                                   "saturday", 
                                                   "sunday"]})

