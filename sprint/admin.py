from django.contrib import admin
from .models import Sprint, Story

# Register your models here.

class ListandoSprints(admin.ModelAdmin):
    list_display = ('id', 'type', 'number')
    list_display_links = ('id', 'type', 'number')
    search_fields = ('type', 'number')
    list_per_page = 10

class ListandoStories(admin.ModelAdmin):
    list_display = ('id', 'sprint', 'ticket_number')
    list_display_links = ('id', 'sprint', 'ticket_number')
    search_fields = ('sprint', 'ticket_number')
    list_per_page = 10

admin.site.register(Sprint, ListandoSprints)
admin.site.register(Story, ListandoStories)