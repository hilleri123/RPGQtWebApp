from django.urls import path
from game_manager import views

urlpatterns = [
    path('', views.index, name='index'),
    
    # SkillGroup URLs
    path('skillgroups/', views.SkillGroupListView.as_view(), name='skillgroup_list'),
    path('skillgroups/add/', views.SkillGroupCreateView.as_view(), name='skillgroup_create'),
    path('skillgroups/<int:pk>/edit/', views.SkillGroupUpdateView.as_view(), name='skillgroup_update'),
    path('skillgroups/<int:pk>/delete/', views.SkillGroupDeleteView.as_view(), name='skillgroup_delete'),
    
    # GameItem URLs
    path('gameitems/', views.GameItemListView.as_view(), name='gameitem_list'),
    path('gameitems/add/', views.GameItemCreateView.as_view(), name='gameitem_create'),
    path('gameitems/<int:pk>/edit/', views.GameItemUpdateView.as_view(), name='gameitem_update'),
    path('gameitems/<int:pk>/delete/', views.GameItemDeleteView.as_view(), name='gameitem_delete'),
    
    # ... аналогичные URL для других моделей ...
]

# rpg_scenario_manager/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('game_manager.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)