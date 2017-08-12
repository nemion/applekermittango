from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required

@login_required
def account(request):
    username = None
    if request.user.is_authenticated():
        username = request.user.username
    return render(request, 'authentication/account.html')