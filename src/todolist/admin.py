from django.contrib import admin

from .models import Category,TodoList
# Register your models here.

admin.site.site_header = "Event Management Administration"
admin.site.site_title = "Event Management Admin Portal"
admin.site.index_title = "Welcome to Event Management Admin Portal"

class TodoListAdmin(admin.ModelAdmin):
    list_display = ("title",  "created", "due_date")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)

admin.site.register(TodoList, TodoListAdmin)
admin.site.register(Category, CategoryAdmin)

