from django.shortcuts import render, redirect
from website import models
from website.utils.pagination import Pagination
from website.utils.form import UserModelForm

def user_list(request):
    # for i in range(100, 200):
    #     models.Employee.objects.create(name='user'+str(i), dept_id=1, gender=2, age=20, create_time='2022-12-12 00:00:00')
 
    data_dict = {}
    search_value = request.GET.get('q')

    if search_value:
        data_dict["name__contains"] = search_value
    else:
        search_value = ''

    query_set = models.Employee.objects.filter(**data_dict)
    page_obj = Pagination(request, query_set)
    query_set = page_obj.query_set
    page_string = page_obj.html()
    return render(request, 'user_list.html', 
        {'query_set': query_set, "search_value": search_value, "page_string": page_string})


def user_add(request):
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'user_add.html', {'form': form})

    form = UserModelForm(data=request.POST)
    
    if form.is_valid():
        form.save()
        return redirect('/user/list/')

    return render(request, 'user_add.html', {'form': form})


def user_edit(request, nid):
    row_obj = models.Employee.objects.filter(id=nid).first()
    if request.method == 'GET':
        form = UserModelForm(instance=row_obj)

        return render(request, 'user_edit.html', {"form": form})

    form = UserModelForm(data=request.POST, instance=row_obj)
    
    if form.is_valid():
        form.save()
        return redirect('/user/list/')

    return render(request, 'user_add.html', {'form': form})


def user_delete(request, nid):
    models.Employee.objects.filter(id=nid).delete()

    return redirect('/user/list')

