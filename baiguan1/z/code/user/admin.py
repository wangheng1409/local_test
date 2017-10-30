from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.core.urlresolvers import reverse

from .models import *
from .forms import *

UserAdmin.list_display =   ('first_name', 'last_name', )

class CMUserAdmin(UserAdmin):
    form = CMUserChangeForm
    add_form = CMUserCreationForm
    # fieldsets = (
    #     ('Basic', {'fields': ('last_open_app', 'is_verified', 'instagram_id',  'role', 'phone', 'profile_image', 'popular_score', 'default_address', 'default_payment', 'default_currency', 'last_read_activity')}),
    #     ('Fashionista', {'fields': ('location', 'tagline', 'tagline_cn', 'pax_card_no', 'cover_image', 'poster_image', 'poster_image_cn', 'fashionista_status')}),
    #     ('StyleProfile', {'fields': ('user_quiz_score', 'fashionista_quiz_score', 'languages', 'brands', 'height', 'weight', 'waist', 'age_range')}),
    # ) + UserAdmin.fieldsets
    # list_display = ('id', 'sync_instagram', 'is_verified', 'first_name', 'last_name', 'bookmarks', 'cards', 'push', 'popular_score', 'phone', 'role', 'default_currency', 'date_joined', 'last_open_app')
    # search_fields = ('id', 'phone', 'first_name', 'last_name')
    # raw_id_fields = ('default_address', 'default_payment')
    # filter_horizontal = ('languages', 'brands')
    list_filter = UserAdmin.list_filter

admin.site.register(CMUser, CMUserAdmin)