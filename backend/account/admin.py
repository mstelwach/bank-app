from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from account.forms import UserUpdateForm, UserCreateForm
from account.models import User, BankAccount


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserUpdateForm
    add_form = UserCreateForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name', 'last_name', 'phone', 'is_admin', )
    list_filter = ('is_admin', 'last_name', 'phone')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone')}),
        ('Permissions', {'fields': ('is_admin', 'is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'phone'),
        }),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)


class AccountBankAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_type', 'sort_code', 'number', 'currency', 'current_balance', )
    list_filter = ('account_type', 'currency')
    fieldsets = (
        ('User account', {'fields': ('user', )}),
        ('Account type', {'fields': ('account_type', 'sort_code', 'number')}),
        ('Account info', {'fields': ('currency', 'current_balance')})
    )
    search_fields = ('user', )
    ordering = ('user', 'current_balance', 'sort_code', )
    filter_horizontal = ()


admin.site.register(BankAccount, AccountBankAdmin)