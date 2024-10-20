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
from DsixRPGcompanionBE.views.auth import register_user, check_user
from rest_framework import routers
from DsixRPGcompanionBE.views.users import UserView
from DsixRPGcompanionBE.views.characters import CharacterView
from DsixRPGcompanionBE.views.skills import SkillView
from DsixRPGcompanionBE.views.archetypes import ArchetypeView
from DsixRPGcompanionBE.views.character_group import CharacterGroupView
from DsixRPGcompanionBE.views.special_ability import SpecialAbilityView
from DsixRPGcompanionBE.views.species import SpeciesView
from DsixRPGcompanionBE.views.notes import NoteView
from DsixRPGcompanionBE.views.csrf import csrf_view

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'notes', NoteView, 'note')
router.register(r'users', UserView, 'user')
router.register(r'heros', CharacterView, 'hero')
router.register(r'skills', SkillView, 'skill')
router.register(r'species', SpeciesView, 'species')
router.register(r'archetypes', ArchetypeView, 'archetype')
router.register(r'specialabilities', SpecialAbilityView, 'specialabilities')
router.register(r'charactergroups', CharacterGroupView, basename='charactergroup')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('checkuser', check_user, name='checkuser'),
    path('register', register_user),
    path('csrf-token/', csrf_view, name='csrf-token'),
    path('heros/add-or-update-character-skills/', CharacterView.as_view({'post': 'add_or_update_character_skills', 'put': 'add_or_update_character_skills'}), name='add-or-update-character-skills'),
    path('heros/<int:pk>/update-skill-code/', CharacterView.as_view({'put': 'update_skill_code'}), name='update-skill-code'),
    path('heros/<int:pk>/skills/', CharacterView.as_view({'get': 'get_skills_for_character'}), name='get-character-skills'),
    path('heros/<int:character_id>/skills/<int:skill_id>/', CharacterView.as_view({'delete': 'remove_skill_from_character'})),
    path('charactergroups/<int:pk>/add_character/', CharacterGroupView.as_view({'post': 'add_character'}), name='charactergroup-add-character'),
    path('charactergroups/<int:pk>/add_characters/', CharacterGroupView.as_view({'post': 'add_characters'}), name='charactergroup-add-characters'),
    path('charactergroups/<int:pk>/remove_character/', CharacterGroupView.as_view({'post': 'remove_character'}), name='charactergroup-remove-character'),
    path('charactergroups/<int:pk>/remove_characters/', CharacterGroupView.as_view({'post': 'remove_characters'}), name='charactergroup-remove-characters'),
    path('', include(router.urls)),
]
