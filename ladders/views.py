from django.shortcuts import redirect, render
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
            form.save()
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
    obj_list=Ladder.objects.all()
    context={
        'obj_list':obj_list
    }
    return render(request,'ladders/gallery.html',context)