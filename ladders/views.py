from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage

from .forms import LadderForm
from .models import Ladder

# Create your views here.
@login_required
def upload_view(request):
    if request.method =='POST':
        form=LadderForm(request.POST,request.FILES)
        if form.is_valid():
            instance=form.save(commit=False)
            instance.user_name = request.user
            instance.save()
            return redirect('/gallery/')
    else:
        form=LadderForm()
    context={
        'form':form
    }
    # if request.method=='POST':
    #     uploaded_file=request.FILES['document']
    #     print(uploaded_file.name)
    #     print(uploaded_file.size)
    #     print(uploaded_file.content_type)
    #     print(uploaded_file.content_type_extra)
        
    #     fs=FileSystemStorage()
    #     name=fs.save(uploaded_file.name,uploaded_file)
    #     context['url']=fs.url(name)
    return render(request,'ladders/upload.html',context)

@login_required
def gallery_view(request):
    # print("Lakhi1",request.method)
    ################
    query_dict=request.GET
    query=query_dict.get('q')
    obj_list=Ladder.objects.filter(user_name=request.user)
    if query is not None:
        obj_list=obj_list.filter(description__icontains=query)
    #####################
    # else:
    #     obj_list=Ladder.objects.filter(user_name=request.user)
    context={
        'obj_list':obj_list
    }
    return render(request,'ladders/gallery.html',context)

@login_required
def detail_view(request,id=None):
    gallery_obj=None
    if id is not None:
        gallery_obj=Ladder.objects.filter(user_name=request.user).get(id=id)
    context={
        "obj":gallery_obj
    }
    return render(request,'ladders/detail.html',context)


@login_required
def update_view(request):
    context={}
    return render(request,'ladders/detail.html',context)

# @login_required
# def search_view(request):
#     query_dict=request.GET
#     query=query_dict.get('q')
#     obj_list=None
#     if query is not None:
#         obj_list=Ladder.objects.get(id=query)
#     context={
#         'obj_list':obj_list
#     }
#     print("Hii")
#     return render(request,'ladders/gallery.html',context)