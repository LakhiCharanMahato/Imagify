from django.shortcuts import render
from accounts.models import User
from django.conf import settings
from .models import FriendList

# Create your views here.
def friends_finder_view(request):
    current_user=request.user
    # usersall=getattr(settings.AUTH_USER_MODEL,str)


    query_dict=request.GET
    if request.method=='GET':
        query=query_dict.get('initialreceiver')
        print("LakhiOK",query,type(query))
        if query:
            user2=User.objects.get(id=int(query))
            friendsalready=FriendList.objects.filter(user1=current_user).filter(user2=user2).exists()
            if not friendsalready:    
                FriendList.send_friend_request(request.user,user2)

    # obj=User.objects.all().exclude(username=current_user)
    obj1=User.objects.all().exclude(username=current_user).values_list('id',flat=True)
    obj2=FriendList.objects.filter(user1=current_user).filter(is_active=False).values_list('user2',flat=True)
    obj3=FriendList.objects.filter(user2=current_user).filter(is_active=True).values_list('user1',flat=True)

    diff=set(obj1)-set(obj2)-set(obj3)
    obj=[]
    for i in diff:
        obj.append(User.objects.get(id=i))

    print(obj)
    context={
        'obj':obj,
        'FriendRequestList':FriendList.objects.filter(user1=current_user).filter(is_active=True).values_list('user2',flat=True)
    }


            # context['FriendRequestList']=FriendList.objects.filter(user1=current_user).values_list('user2',flat=True)
            # return render(request,'friends/finder.html',context)




    return render(request,'friends/finder.html',context)

def friend_request_received_view(request):
    current_user=request.user

    query_dict=request.GET
    if request.method=='GET':
        query=query_dict.get('acceptrequest')
        # print("LakhiOK",query,type(query))
        query1=query_dict.get('deleterequest')
        if query:
            user1=User.objects.get(id=int(query))
            friendsalready=FriendList.objects.filter(user1=user1).filter(user2=current_user).filter(is_active=False).exists()
            if not friendsalready:    
                FriendList.accept_friend_request(user1,request.user)

        if query1:
            user1=User.objects.get(id=int(query1))
            friendsalready=FriendList.objects.filter(user1=user1).filter(user2=current_user).filter(is_active=False).exists()
            friendrequestexists=FriendList.objects.filter(user1=user1).filter(user2=current_user).filter(is_active=True).exists()
            if not friendsalready and friendrequestexists:
                FriendList.delete_friend_request(user1,request.user)            


    obj1=FriendList.objects.filter(user2=current_user).filter(is_active=True).values_list('user1',flat=True)
    obj1=set(obj1)

    obj=[]
    for i in obj1:
        obj.append(User.objects.get(id=i))
    context={
        'obj':obj
    }
    return render(request,'friends/allrequests.html',context)


def my_friends_all_view(request):
    current_user=request.user
    obj1=FriendList.objects.filter(user1=current_user).filter(is_active=False).values_list('user2',flat=True)
    obj1=set(obj1)

    obj=[]
    for i in obj1:
        obj.append(User.objects.get(id=i))
    context={
        'obj':obj
    }
    return render(request,'friends/allfriends.html',context)
