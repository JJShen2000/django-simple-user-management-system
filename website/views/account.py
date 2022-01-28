from django.shortcuts import render, redirect
from website.utils.form import LoginModelForm
from website import models


def login(request):
    if request.method == 'GET':
        form = LoginModelForm()
        return render(request, 'login.html', {'form': form})
    form = LoginModelForm(data=request.POST)
    
    if form.is_valid():
        admin_obj = models.Admin.objects.filter(**form.cleaned_data).first()
        if not admin_obj:
            form.add_error("password", "User name or password is error")
            return render(request, "login.html", {'form': form})
        request.session['info'] = {"id": admin_obj.id, 'user_name': admin_obj.user_name}
        return redirect('/admin/list')

    # invalid
    return render(request, "login.html", {'form': form})

def logout(request):
    request.session.clear()
    return redirect('/login/')