from django.contrib import admin
from .models import taskdetails, userprofile,cart


# Register your models here.

class userprofileAdmin(admin.ModelAdmin):
    list_display = ('address', 'city', 'state')

admin.site.register(userprofile, userprofileAdmin)  


#Admin panel me taskdetails model kaisa dikhega, woh yeh class decide karegi

class taskdetailsAdmin(admin.ModelAdmin):
    list_display = (
        'title',          # task_title ko replace kiya
        'created_by',     # task_created_by
        'closed_by',      # task_closed_by
        'assigned_to',    # task_holder
        'description',    # task_description
         'task_status',    # task_status sahi hai
    )

admin.site.register(taskdetails, taskdetailsAdmin)

class cartAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'task_count')

admin.site.register(cart, cartAdmin)