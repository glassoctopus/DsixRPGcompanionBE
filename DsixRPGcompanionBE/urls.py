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

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'users', UserView, 'user')
router.register(r'heros', CharacterView, 'hero')
router.register(r'skills', SkillView, 'skill')
router.register(r'archetypes', ArchetypeView, 'archetype')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('checkuser', check_user, name='checkuser'),
    path('register', register_user),
    path('heros/character-skills', CharacterView.add_skill_to_character, name='add-skill-to-character'),
    path('heros/<int:character_id>/skills/', CharacterView.as_view({'get': 'retrieve_character_with_skills'}), name='character-with-skills'),
     path('heros/<int:pk>/update-skill-code/', CharacterView.as_view({'put': 'update_skill_code'}), name='update-skill-code'),
    path('', include(router.urls)),
]
