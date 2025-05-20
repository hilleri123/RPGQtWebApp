from django import forms
from .models import *
import json

class JSONFieldForm(forms.ModelForm):
    """Базовый класс для форм с JSON-полями"""
    def clean_json_field(self, field_name, json_field_name):
        data = self.cleaned_data[field_name]
        if not data:
            return '{}'
        try:
            json.loads(data)
            return data
        except json.JSONDecodeError:
            raise forms.ValidationError(f"Некорректный формат JSON в поле {field_name}")

class GameItemForm(JSONFieldForm):
    bonuses = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False,
                            help_text='Введите бонусы в формате JSON')
    
    class Meta:
        model = GameItem
        fields = ['name', 'text', 'bonuses']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.bonuses_json:
            try:
                self.fields['bonuses'].initial = json.dumps(json.loads(self.instance.bonuses_json), indent=2)
            except:
                self.fields['bonuses'].initial = self.instance.bonuses_json
    
    def clean_bonuses(self):
        return self.clean_json_field('bonuses', 'bonuses_json')
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.bonuses_json = self.cleaned_data['bonuses']
        if commit:
            instance.save()
        return instance

class NPCForm(JSONFieldForm):
    skill_ids = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=False,
                             help_text='Введите ID навыков в формате JSON')
    
    class Meta:
        model = NPC
        fields = ['name', 'path_to_img', 'is_enemy', 'skill_ids', 'description', 'is_dead']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk and self.instance.skill_ids_json:
            try:
                self.fields['skill_ids'].initial = json.dumps(json.loads(self.instance.skill_ids_json), indent=2)
            except:
                self.fields['skill_ids'].initial = self.instance.skill_ids_json
    
    def clean_skill_ids(self):
        return self.clean_json_field('skill_ids', 'skill_ids_json')
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.skill_ids_json = self.cleaned_data['skill_ids']
        if commit:
            instance.save()
        return instance