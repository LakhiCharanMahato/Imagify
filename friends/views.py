from django.shortcuts import render
from accounts.models import User
from django.conf import settings
from .models import FriendList

# Create your views here.
def friends_finder_view(request):
    current_user=request.user
    # usersall=getattr(settings.AUTH_USER_MODEL,str)

    # obj=User.objects.all().exclude(username=current_user)
    obj1=User.objects.all().exclude(username=current_user).values_list('id',flat=True)
    obj2=FriendList.objects.filter(user1=current_user).values_list('user2',flat=True)
    diff=set(obj1)-set(obj2)
    obj=[]
    for i in diff:
        obj.append(User.objects.get(id=i))

    query_dict=request.GET
    if request.method=='GET':
        query=query_dict.get('initialreceiver')
        print("LakhiOK",query,type(query))
        if query:
            FriendList.send_friend_request(request.user,User.objects.get(id=int(query)))


    print(obj)
    context={
        'obj':obj,
        'FriendList':FriendList
    }
    return render(request,'friends/finder.html',context)
