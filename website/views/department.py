from django.shortcuts import render, redirect
from website import models
from website.utils.pagination import Pagination


def department_list(request):
    query_set = models.Department.objects.all()
    page_obj = Pagination(request, query_set)
    query_set = page_obj.query_set
    page_string = page_obj.html()
    return render(request, 'department_list.html', {'query_set': query_set, "page_string": page_string})

def department_add(request):
    if request.method == 'GET':
        return render(request, 'department_add.html')
    title = request.POST.get('title')
    models.Department.objects.create(title=title)

    return redirect('/department/list')

def department_delete(request):
    nid = request.GET.get('nid')
    models.Department.objects.filter(id=nid).delete()

    return redirect('/department/list')

def department_edit(request, nid):
    if request.method == 'GET':
        obj = models.Department.objects.filter(id=nid).first()
        return render(request, 'department_edit.html', {"obj": obj})
    
    title = request.POST.get('title')
    models.Department.objects.filter(id=nid).update(title=title)

    return redirect('/department/list')