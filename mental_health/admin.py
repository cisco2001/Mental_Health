from django.contrib import admin
from .models import Student, Appointment, Staff
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django import forms


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'university')
    search_fields = ('first_name', 'last_name', 'email', 'university')

class StaffAdmin(UserAdmin):
    model = Staff
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(Staff, StaffAdmin)

class AppointmentAdminForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['student', 'staff', 'date', 'text', 'status', 'remarks']
        widgets = {
            'date': forms.SelectDateWidget(),
        }

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'staff', 'date', 'text', 'status', 'remarks')
    list_filter = ('status', 'date')
    search_fields = ('student__first_name', 'student__last_name', 'staff__first_name', 'staff__last_name')
    actions = ['approve_appointments', 'reject_appointments']
    
    def approve_appointments(self, request, queryset):
        queryset.update(status='A')
        self.message_user(request, "Selected appointments have been approved.")
    approve_appointments.short_description = "Approve selected appointments"
    
    def reject_appointments(self, request, queryset):
        queryset.update(status='R')
        self.message_user(request, "Selected appointments have been rejected.")
    reject_appointments.short_description = "Reject selected appointments"

admin.site.unregister(Group)

admin.site.site_header = "Uni Therapy Admin"
admin.site.site_title = "Uni Therapy Admin Portal"
admin.site.index_title = "Welcome to Uni Therapy Admin Portal"