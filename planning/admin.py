from django.contrib import admin
from .models import Planning, PlanningParticipant, PokerRound, Vote

# Register your models here.

class ListandoPlanning(admin.ModelAdmin):
    list_display = ('id', 'sprint')
    list_display_links = ('id', 'sprint')
    search_fields = ('sprint', 'date')
    list_per_page = 10

class ListandoPlanningParticipant(admin.ModelAdmin):
    list_display = ('id', 'planning', 'participant')
    list_display_links = ('id', 'planning', 'participant')
    search_fields = ('planning', 'participant')
    list_per_page = 10

class ListandoPokerRound(admin.ModelAdmin):
    list_display = ('id', 'planning', 'story', 'avg_points')
    list_display_links = ('id', 'planning', 'story', 'avg_points')
    search_fields = ('planning', 'story', 'avg_points')
    list_per_page = 10

class ListandoVote(admin.ModelAdmin):
    list_display = ('id', 'poker_round', 'participant', 'estimated_points')
    list_display_links = ('id', 'poker_round', 'participant', 'estimated_points')
    search_fields = ('poker_round', 'participant', 'estimated_points')
    list_per_page = 10

admin.site.register(Planning, ListandoPlanning)
admin.site.register(PlanningParticipant, ListandoPlanningParticipant)
admin.site.register(PokerRound, ListandoPokerRound)
admin.site.register(Vote, ListandoVote)