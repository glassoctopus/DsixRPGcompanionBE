"""DsixRPGcompanionBE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from DsixRPGcompanionBE.views.auth import LoginAPIView, RegisterAPIView, UserAPIView, LogoutAPIView, SessionStatusAPIView
from DsixRPGcompanionBE.views.abilities import AbilityViewSet
from DsixRPGcompanionBE.views.archetypes import ArchetypeViewSet
from DsixRPGcompanionBE.views.audit_logs import AuditLogViewSet
from DsixRPGcompanionBE.views.character_groups import CharacterGroupViewSet
from DsixRPGcompanionBE.views.characters import CharacterViewSet
from DsixRPGcompanionBE.views.notes import NoteViewSet
from DsixRPGcompanionBE.views.skills import SkillViewSet
from DsixRPGcompanionBE.views.species import SpeciesViewSet
from DsixRPGcompanionBE.views.users import UserViewSet

router = routers.DefaultRouter()
router.register(r'notes', NoteViewSet, 'note')
router.register(r'users', UserViewSet, 'user')
router.register(r'heros', CharacterViewSet, 'hero')
router.register(r'skills', SkillViewSet, 'skill')
router.register(r'species', SpeciesViewSet, basename='species')
router.register(r'archetypes', ArchetypeViewSet, 'archetype')
router.register(r'abilities', AbilityViewSet, 'abilities')
router.register(r'charactergroups', CharacterGroupViewSet, basename='charactergroup')
router.register(r'audit-logs', AuditLogViewSet, basename='auditlog')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('api/register/', RegisterAPIView.as_view(), name='register'),
    path('api/logout/', LogoutAPIView.as_view(), name='logout'),
    path('api/session-status/', SessionStatusAPIView.as_view(), name='session-status'),
    path('api/user/', UserAPIView.as_view(), name='user'),
    path('heros/add-or-update-character-skills/', CharacterViewSet.as_view({'post': 'add_or_update_character_skills', 'put': 'add_or_update_character_skills'}), name='add-or-update-character-skills'),
    path('heros/<int:pk>/update-skill-code/', CharacterViewSet.as_view({'put': 'update_skill_code'}), name='update-skill-code'),
    path('heros/<int:pk>/skills/', CharacterViewSet.as_view({'get': 'get_skills_for_character'}), name='get-character-skills'),
    path('heros/<int:character_id>/skills/<int:skill_id>/', CharacterViewSet.as_view({'delete': 'remove_skill_from_character'})),
    path('charactergroups/<int:pk>/add_character/', CharacterGroupViewSet.as_view({'post': 'add_character'}), name='charactergroup-add-character'),
    path('charactergroups/<int:pk>/add_characters/', CharacterGroupViewSet.as_view({'post': 'add_characters'}), name='charactergroup-add-characters'),
    path('charactergroups/<int:pk>/remove_character/', CharacterGroupViewSet.as_view({'post': 'remove_character'}), name='charactergroup-remove-character'),
    path('charactergroups/<int:pk>/remove_characters/', CharacterGroupViewSet.as_view({'post': 'remove_characters'}), name='charactergroup-remove-characters'),
    path('', include(router.urls)),
]
