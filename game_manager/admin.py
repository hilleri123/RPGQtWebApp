from django.contrib import admin
from .models import *

@admin.register(SkillGroup)
class SkillGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'group')
    list_filter = ('group',)
    search_fields = ('name',)

@admin.register(GameItem)
class GameItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name', 'text')

@admin.register(NPC)
class NPCAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_enemy', 'is_dead')
    list_filter = ('is_enemy', 'is_dead')
    search_fields = ('name', 'description')

@admin.register(SceneMap)
class SceneMapAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'file_path')
    search_fields = ('name',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'leads_to')
    list_filter = ('leads_to',)
    search_fields = ('name', 'description')

@admin.register(PlayerCharacter)
class PlayerCharacterAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'map', 'location', 'player_locked')
    list_filter = ('map', 'location', 'player_locked')
    search_fields = ('name', 'short_desc')

class StatInline(admin.TabularInline):
    model = Stat
    extra = 1

@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('character', 'skill', 'init_value', 'value')
    list_filter = ('character', 'skill')

@admin.register(WhereObject)
class WhereObjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'game_item', 'npc', 'location', 'player')
    list_filter = ('location', 'npc')

@admin.register(GlobalSession)
class GlobalSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'scenario_name', 'time', 'start_time')
    search_fields = ('scenario_name', 'intro')

@admin.register(PlayerAction)
class PlayerActionAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'is_activated', 'add_time_secs')
    list_filter = ('is_activated',)
    search_fields = ('description',)

@admin.register(MapObjectPolygon)
class MapObjectPolygonAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'map', 'location', 'is_shown')
    list_filter = ('map', 'location', 'is_shown', 'is_filled', 'is_line')
    search_fields = ('name',)

@admin.register(GameEvent)
class GameEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'happened', 'start_time', 'end_time')
    list_filter = ('happened',)
    search_fields = ('name',)

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'action')
    list_filter = ('action',)
    search_fields = ('name', 'xml_text')