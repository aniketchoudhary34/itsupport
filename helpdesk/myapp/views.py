
from django.http import HttpResponse
from .models import Task
from django.shortcuts import render,redirect

from .models import taskdetails, userprofile,cart
from .forms import LoginForm, registerForm, taskdetailform, userprofileform
from django.contrib.auth import authenticate, login,logout
from django.shortcuts import redirect, render   
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.views import PasswordResetView
from .forms import CustomPasswordResetForm 
from django.db.models import Q
import openpyxl
from django.utils.timezone import now
from datetime import timedelta








# Create your views here. 

# def baseview(request):
#     if request.user.is_authenticated:  # Check if the user is logged in
#         tasktedetas = taskdetails.objects.all()  # Fetch all taskdetails from the database
#         return render(request, 'base.html', {'tasktedetas': tasktedetas})
#     # render the 'base.html' template returning the HTTP response (render = "HTML page ko open karke user ko bhejna")
#     else:
#         return redirect('login')  # Redirect to login page if not logged in

from datetime import timedelta
from django.utils.timezone import now
from django.db.models import Q

@login_required
def baseview(request):

    status_filter = request.GET.get("status")
    search_query = request.GET.get("search")
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    tasks = taskdetails.objects.all().order_by("-created_on")

    # 🔹 Status filter
    if status_filter:
        tasks = tasks.filter(task_status=status_filter)

    # 🔹 Search filter (title / description / id)
    if search_query:
        tasks = tasks.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(id__icontains=search_query)
        )

    # 🔹 Date filter
    if start_date and end_date:
        tasks = tasks.filter(
            created_on__date__range=[start_date, end_date]
        )
    else:
        # 👉 Default: last 7 days
        last_7_days = now() - timedelta(days=7)
        tasks = tasks.filter(created_on__gte=last_7_days)

    context = {
        "tasktedetas": tasks,

        "new_count": taskdetails.objects.filter(task_status="new").count(),
        "inprogress_count": taskdetails.objects.filter(task_status="in_progress").count(),
        "completed_count": taskdetails.objects.filter(task_status="completed").count(),
        "closed_count": taskdetails.objects.filter(task_status="closed").count(),

        "active_filter": status_filter,
        "search_query": search_query,
        "start_date": start_date,
        "end_date": end_date,
    }

    return render(request, "base.html", context)


 
# def login_view(request): #Ye view function hota hai.
                   
                    
   
#     if request.method == 'POST': #Jab user form submit kare (Data server ko bhejta hai)
       
#         Forms=LoginForm(request.POST) #Ye Django ko batata hai ki user ne jo form submit kiya hai, wo LoginForm ke format me aa chuka hai.
       
#         if Forms.is_valid():  #empty toh nahi?  password empty toh nahi? # Process the form data (e.g., authenticate user)
#             username = Forms.cleaned_data['username']
#             password = Forms.cleaned_data['password']   # Authentication logic goes here # User ko check karo
#             user=authenticate(request, username=username, password=password)
        
#             if user is not None:
#                 login(request,user)  # User ko login kar do
#                 messages.success(request,"Login Successful")         
#                 return redirect('base')

#             else:
#                 messages.error(request,"username or password not valid")
#                 return render(request,'login.html')
#     else: #Jab user pehli baar form ko access kare (GET request)
#         Forms=LoginForm()  #Jab user pehli baar form ko access kare (GET request)    
#     return render(request,'login.html', {'Forms': Forms})  #Form ko HTML page me bhejo taki user usko fill kar sake

def login_view(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Login Successful")
                return redirect('base')   # ✅ kisi view ka URL name
            else:
                messages.error(request, "Username or password incorrect")

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, "Logout Successful")
    return redirect('login')

def register_view(request):
    if request.method == 'POST':
        register_form = registerForm(request.POST)
        user_profile_form = userprofileform(request.POST)
        if register_form.is_valid() and user_profile_form.is_valid():
            registerform=register_form.save() 
            user_profile = user_profile_form.save(commit=False)
            address =  user_profile_form.cleaned_data['address']
            city =  user_profile_form.cleaned_data['city']
            state = user_profile_form.cleaned_data['state']
            profile=userprofile(user=registerform, address=address, city=city, state=state)
            profile.save()
            messages.success(request, "Registration Successful")
            return redirect('login')
        else:
            messages.error(request, "Registration Unsuccessful. Invalid information.")
            return render(request, 'Register.html', {'register_form': register_form, 'user_profile_form': user_profile_form})
    else:
        register_form = registerForm()
        user_profile_form = userprofileform()
    return render(request, 'Register.html', {'register_form': register_form, 'user_profile_form': user_profile_form})


#user profile
@login_required
def user_profile(request):
    profile, created = userprofile.objects.get_or_create(user=request.user)

    context = {
        'profile': profile
    }
    return render(request, 'userprofile.html', context)
    

#update profile can be added similarly
@login_required
def update_profile(request,pk):
    if request.user.is_authenticated:
        profile=userprofile.objects.get(id=pk)
        form=userprofileform(request.POST or None, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile Updated Successfully")
            return redirect('user_profile')
        return render(request, 'update_profile.html', {'form': form})
    else:
        return redirect('login')
    
#task details view can be added similarly
@login_required
def taskdetails_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    if request.method == 'POST':
        form = taskdetailform(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user  # set current logged-in user
            task.save()
            messages.success(request, "Task Created Successfully")
            return redirect('taskdetails')  # redirect to same page or dashboard
    else:
        form = taskdetailform()

    # Fetch all tasks to show in dashboard
    tasks = taskdetails.objects.all()
    return render(request, 'taskdetails.html', {'form': form, 'tasktedetas': tasks})

#task infor
@login_required
def task_info(request,pk):
    if request.user.is_authenticated:
        task=taskdetails.objects.get(id=pk)
        return render(request, 'task_info.html', {'task': task})
    else:
        return redirect('login') 
    

#update task details can be added similarly
@login_required
def update_task(request,pk):
    if request.user.is_authenticated:
        task=taskdetails.objects.get(id=pk)
        form=taskdetailform(request.POST or None, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task Updated Successfully")
            return redirect('base')
        return render(request, 'update_task.html', {'form': form})
    else:
        return redirect('login')
    
#delete task details can be added similarly
@login_required
def deletetask(request,pk):
    if request.user.is_authenticated:
        task=taskdetails.objects.get(id=pk)
        task.delete()
        messages.success(request, "Task Deleted Successfully")
        return redirect('base')
    else:
        return redirect('login')
    

#MYCART
@login_required
def mycarts(request):
    currentuser = request.user

    if currentuser.is_staff:
        # Staff sees all tasks they approved or assigned
        cartitems = taskdetails.objects.filter(task_status__in=["approved", "in_progress", "completed", "closed"])
    else:
        # Normal user sees all tasks they created
        cartitems = taskdetails.objects.filter(created_by=currentuser)

    return render(request, 'mycart.html', {'cartitems': cartitems})

    
#accept task can be added similarly
@login_required
def accept_task(request, pk):
    task = get_object_or_404(taskdetails, pk=pk)

    if task.task_status != "new":
        messages.error(request, "Task already accepted")
        return redirect("base")

    task.task_status = "in_progress"
    task.assigned_to = request.user
    task.save()

    messages.success(request, "Task accepted")
    return redirect("base")


#remove from cart can be added similarly
@login_required
def remove_task(request,pk):
    if request.user.is_authenticated:
        ctaskdatas=taskdetails.objects.get(id=pk)
        ctaskdatas.task_status='Open'
        ctaskdatas.save()

        cartitem=cart.objects.filter(id=pk)
        cartitem.delete()
        messages.success(request, "Task Removed from Cart Successfully")
        return redirect('mycart')
    else:
        return redirect('login')


@staff_member_required
def add_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # 🔴 Username check
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, "add_user.html")

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, "User added successfully!")
        return render(request, "add_user.html")

    return render(request, "add_user.html")

@login_required
def mark_done(request, pk):
    task = get_object_or_404(
        taskdetails,
        pk=pk,
        assigned_to=request.user
    )

    if task.task_status != "in_progress":
        messages.error(request, "Task not in progress")
        return redirect("base")

    task.task_status = "completed"
    task.save()

    messages.success(request, "Task completed")
    return redirect("base")




@staff_member_required
def user_list(request):
    users = User.objects.all()
    total_users = users.count()
    return render(request, 'user_list.html', {
        'users': users,
        'total_users': total_users
    })

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:  # ✅ Inactive users blocked
                login(request, user)
                return redirect('home')  # successful login
            else:
                messages.error(request, "Your account is inactive. Contact admin.")
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    template_name = 'password_reset.html'



def toggle_user_status(request, user_id):
    if not request.user.is_staff:
        messages.error(request, "Only admin can change status.")
        return redirect('user_list')  # Your user list page

    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active  # Toggle status
    user.save()
    
    messages.success(request, f"{user.username} is now {'Active' if user.is_active else 'Inactive'}.")
    return redirect('user_list')



@login_required
def create_task(request):
    if request.method == "POST":
        print("FILES:", request.FILES)  # 🔥 DEBUG LINE

        form = taskdetailform(request.POST, request.FILES)

        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()

            messages.success(request, "Task created successfully")
            return redirect('base')
        else:
            print("FORM ERRORS:", form.errors)
    else:
        form = taskdetailform()

    return render(request, 'create_task.html', {'form': form})



@login_required
def close_task(request, pk):
    task = get_object_or_404(
        taskdetails,
        pk=pk,
        created_by=request.user
    )

    if task.task_status != "completed":
        messages.error(request, "Task not ready to close")
        return redirect("base")

    task.task_status = "closed"
    task.closed_by = request.user
    task.save()

    messages.success(request, "Task closed successfully")
    return redirect("base")


@staff_member_required
def manage_users(request):
    users = User.objects.all()
    return render(request, "manage_users.html", {"users": users})



@staff_member_required
def update_user_role(request, user_id):
    user = User.objects.get(id=user_id)

    if request.method == "POST":
        user.groups.clear()

        if request.POST.get("task_creator"):
            group = Group.objects.get(name="task_creator")
            user.groups.add(group)

        if request.POST.get("worker"):
            group = Group.objects.get(name="worker")
            user.groups.add(group)

        return redirect("manage_users")

    return render(request, "update_user_role.html", {"user": user})


@login_required
def close_task(request, pk):
    task = get_object_or_404(
        taskdetails,
        pk=pk,
        created_by=request.user
    )

    if task.task_status != "completed":
        messages.error(request, "Task not ready to close")
        return redirect("base")

    task.task_status = "closed"
    task.closed_by = request.user
    task.save()

    messages.success(request, "Task closed successfully")
    return redirect("base")



# @login_required
# def task_report(request):

#     tasks = taskdetails.objects.all().order_by("-created_on")
#     users = User.objects.all()

#     # FILTERS
#     user_id = request.GET.get("user")
#     status = request.GET.get("status")
#     ticket_id = request.GET.get("ticket")
#     start_date = request.GET.get("start_date")
#     end_date = request.GET.get("end_date")

#     if user_id and user_id != "all":
#         tasks = tasks.filter(created_by_id=user_id)

#     if status and status != "all":
#         tasks = tasks.filter(task_status=status)

#     if ticket_id:
#         tasks = tasks.filter(id=ticket_id)

#     if start_date and end_date:
#         tasks = tasks.filter(
#             created_on__date__range=[start_date, end_date]
#         )

#     context = {
#         "tasks": tasks,
#         "users": users
#     }
#     return render(request, "task_report.html", context)


@login_required
def report_download(request):
    tasks = apply_report_filters(request)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Task Report"

    headers = [
        "Ticket ID", "Title", "User", "Status",
        "Created On", "Due Date", "Reward"
    ]
    ws.append(headers)

    for t in tasks:
        ws.append([
            t.id,
            t.title,
            t.created_by.username,
            t.task_status,
            t.created_on.strftime("%d-%m-%Y"),
            t.due_date.strftime("%d-%m-%Y"),
            t.reward
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = "attachment; filename=task_report.xlsx"
    wb.save(response)
    return response


@login_required
def report_criteria(request):
    users = User.objects.all()
    return render(request, "reports/criteria.html", {"users": users})


def apply_report_filters(request):
    tasks = taskdetails.objects.all()

    user = request.GET.get("user")
    status = request.GET.get("status")
    ticket = request.GET.get("ticket")
    start = request.GET.get("start_date")
    end = request.GET.get("end_date")

    if user and user != "all":
        tasks = tasks.filter(created_by_id=user)

    if status and status != "all":
        tasks = tasks.filter(task_status=status)

    if ticket:
        tasks = tasks.filter(id=ticket)

    if start and end:
        tasks = tasks.filter(created_on__date__range=[start, end])

    return tasks

@login_required
def report_view(request):
    tasks = apply_report_filters(request)
    return render(request, "reports/view.html", {"tasks": tasks})
