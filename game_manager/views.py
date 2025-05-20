from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import *
from .forms import *

def index(request):
    """Главная страница"""
    context = {
        'skill_groups_count': SkillGroup.objects.count(),
        'skills_count': Skill.objects.count(),
        'game_items_count': GameItem.objects.count(),
        'npcs_count': NPC.objects.count(),
        'characters_count': PlayerCharacter.objects.count(),
        'locations_count': Location.objects.count(),
        'maps_count': SceneMap.objects.count(),
        'events_count': GameEvent.objects.count(),
    }
    return render(request, 'game_manager/index.html', context)

# Представления для SkillGroup
class SkillGroupListView(ListView):
    model = SkillGroup
    context_object_name = 'skill_groups'
    template_name = 'game_manager/skillgroup/list.html'

class SkillGroupCreateView(CreateView):
    model = SkillGroup
    fields = ['name']
    template_name = 'game_manager/skillgroup/form.html'
    success_url = reverse_lazy('skillgroup_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание группы навыков'
        return context

class SkillGroupUpdateView(UpdateView):
    model = SkillGroup
    fields = ['name']
    template_name = 'game_manager/skillgroup/form.html'
    success_url = reverse_lazy('skillgroup_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование группы навыков'
        return context

class SkillGroupDeleteView(DeleteView):
    model = SkillGroup
    template_name = 'game_manager/confirm_delete.html'
    success_url = reverse_lazy('skillgroup_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление группы навыков'
        context['message'] = f'Вы уверены, что хотите удалить группу навыков "{self.object.name}"?'
        return context

# Представления для GameItem
class GameItemListView(ListView):
    model = GameItem
    context_object_name = 'game_items'
    template_name = 'game_manager/gameitem/list.html'

class GameItemCreateView(CreateView):
    model = GameItem
    form_class = GameItemForm
    template_name = 'game_manager/gameitem/form.html'
    success_url = reverse_lazy('gameitem_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание предмета'
        return context

class GameItemUpdateView(UpdateView):
    model = GameItem
    form_class = GameItemForm
    template_name = 'game_manager/gameitem/form.html'
    success_url = reverse_lazy('gameitem_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование предмета'
        return context

class GameItemDeleteView(DeleteView):
    model = GameItem
    template_name = 'game_manager/confirm_delete.html'
    success_url = reverse_lazy('gameitem_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Удаление предмета'
        context['message'] = f'Вы уверены, что хотите удалить предмет "{self.object.name}"?'
        return context