from django.utils import timezone
from datetime import datetime
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse


from .models import TodoList, Category
from .forms import RegistrationForm,TodoForm


@login_required(redirect_field_name='login')
def index(request): #the index view
    user = request.user
    todos = TodoList.objects.filter(user = user) #quering all todos with the object manager
    categories = Category.objects.all() #getting all categories with object manager

    if request.method == "POST": #checking if the request method is a POST
        
        if "taskAdd" in request.POST: #checking if there is a request to add a todo
            due_date_str = request.POST["date"]
            category = request.POST["category_select"]
            
            if(category.strip()):
                if( due_date_str.strip()):
                    due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
                    start_date = datetime.now().date()
                    if (due_date >= start_date):
                        title = request.POST["description"] #title
                        date = due_date_str #date
                        category = request.POST["category_select"] #category
                        content = title + " -- " + date + " -- " + category #content                  
                        Todo = TodoList(
                            title=title, 
                            content=content, 
                            due_date=date, 
                            category=Category.objects.get(name=category),
                            user = user )
                        Todo.save() #saving the todo 
                        return redirect("/") #reloading the page
                    else:
                        messages.warning(request, 'Due Date should not be past.')

                else:
                    messages.warning(request, 'Due Date is requiered.')
            else:
                    messages.warning(request, 'Category is requiered .')


        if "taskDelete" in request.POST: #checking if there is a request to delete a todo
            checkedlist =[]
            checkedlist = request.POST.getlist("checkedbox") #checked todos to be deleted
            if checkedlist :
                for todo_id in checkedlist:
                    todo = TodoList.objects.filter(id=int(todo_id)) #getting todo id
                    todo.delete() #deleting todo
            else:
                messages.warning(request, 'Please select the task.')

    return render(request, "home.html", {"todos": todos, "categories":categories})


@login_required(redirect_field_name='login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('todolist:todo_list')
    else:
        form = RegistrationForm()
    return render(request, 'signup.html', {'form': form})