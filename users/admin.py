from django.contrib import admin
from .models import Profile, CoarseBranch, BuddyRequest 

admin.site.register(CoarseBranch)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    readonly_fields = [field.name for field in Profile._meta.fields]
    readonly_fields.remove('email')      
    readonly_fields.remove('otp')
    readonly_fields.remove('verified')

# @admin.register(BuddyRequest)
# class BuddyRequestAdmin(admin.ModelAdmin):
#     readonly_fields = [field.name for field in BuddyRequest._meta.fields]
