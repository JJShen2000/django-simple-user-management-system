from django.shortcuts import render, redirect
from matplotlib.pyplot import title
from pendulum import instance
from website import models
from website.utils.pagination import Pagination
from website.utils.form import AdminModelForm, AdminEditModelForm, AdminResetModelForm

def admin_list(request):
    query_set = models.Admin.objects.all()
    page_obj = Pagination(request, query_set)
    query_set = page_obj.query_set
    page_string = page_obj.html()
    return render(request, 'admin_list.html', {'query_set': query_set, "page_string": page_string})


def admin_add(request):
    title = 'New Admin'
    if request.method == 'GET':
        form = AdminModelForm()
        return render(request, "add.html", {'form': form, 'title': title})
    
    form = AdminModelForm(data=request.POST)
    
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    return render(request, "add.html", {'form': form, 'title': title})

def admin_edit(request, nid):
    row_obj = models.Admin.objects.filter(id=nid).first()
    if not row_obj:
        return redirect('/admin/list/')
    title = 'Edit Admin'

    if request.method == 'GET':
        form = AdminEditModelForm(instance=row_obj)
        return render(request, "add.html", {'form': form, 'title': title})

    form = AdminEditModelForm(data=request.POST, instance=row_obj)
    
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    # invalid
    return render(request, "add.html", {'form': form, 'title': title})

def admin_delete(request, nid):
    models.Admin.objects.filter(id=nid).delete()

    return redirect('/admin/list')

def admin_reset(request, nid):
    row_obj = models.Admin.objects.filter(id=nid).first()
    if not row_obj:
        return redirect('/admin/list/')
    title = 'Reset Password of {}'.format(row_obj.user_name)

    if request.method == 'GET':
        form = AdminResetModelForm()
        return render(request, "add.html", {'form': form, 'title': title})

    form = AdminResetModelForm(data=request.POST, instance=row_obj)
    
    if form.is_valid():
        form.save()
        return redirect('/admin/list/')

    # invalid
    return render(request, "add.html", {'form': form, 'title': title})


    
