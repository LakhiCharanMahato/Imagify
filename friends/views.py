from django.shortcuts import render
from accounts.models import User
from django.conf import settings

# Create your views here.
def friends_finder_view(request):
    current_user=request.user
    # usersall=getattr(settings.AUTH_USER_MODEL,str)
    obj=User.objects.all().exclude(username=current_user)
    print(obj)
    context={
        'obj':obj
    }
    return render(request,'friends/finder.html',context)
