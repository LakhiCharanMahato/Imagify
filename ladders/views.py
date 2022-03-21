from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator

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
    countobj=obj_list.count()
    #####################
    # else:
    #     obj_list=Ladder.objects.filter(user_name=request.user)
    items_per_page=2
    obj_list_page=[]
    pagescount=countobj//items_per_page
    for i in range(pagescount):
        var1=i*items_per_page
        var2=(i+1)*items_per_page
        obj_list_page.append(obj_list[var1:var2])

    print(obj_list_page,countobj,pagescount)


    paginator = Paginator(obj_list, 1) # Show 25 contacts per page.


    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print("Lakhi",page_obj.number,paginator.count)

    
    if paginator.count > 5:
        empty_list_page=list(range(1,6))
    else:
        empty_list_page=list(range(1,paginator.count+1))



    coun=paginator.count
    context={
        'obj_list':obj_list,
        'countobj':countobj,
        'obj_list_page':obj_list_page,
        'coun':coun,
        'page_obj':page_obj,
        'empty_list_page':empty_list_page
    }
    return render(request,'ladders/gallery.html',context)

@login_required
def detail_view(request,id=None):
    # gallery_obj=None
    # if id is not None:
    #     gallery_obj=Ladder.objects.filter(user_name=request.user).get(id=id)
    gallery_obj=get_object_or_404(Ladder,id=id,user_name=request.user)
    context={
        "obj":gallery_obj
    }
    return render(request,'ladders/detail.html',context)


@login_required
def update_view(request,id=None):
    # print(id,type(id),"Lakhi")
    obj= get_object_or_404(Ladder, id=id, user_name=request.user)
    print(len(request.FILES))
    form=LadderForm(request.POST or None,instance=obj)
    # if request.method =='POST':
    #     form=LadderForm(request.POST,request.FILES)
    #     if form.is_valid():
    #         instance=form.save()
    #         instance.user_name = request.user
    #         instance.save()
    #         context['message']='Data saved.'
    #         # return redirect('/gallery/')
    # else:
    #     form=LadderForm(instance=obj)
    context={
        'form':form,
        "object":obj
    }
    if form.is_valid():
        if len(request.FILES)>0:
            instance=form.save(commit=False)
            instance.file=request.FILES['file']
            instance.save()
        else:
            form.save()
        context['message']='Data saved.'
    return render(request,'ladders/upload.html',context)

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