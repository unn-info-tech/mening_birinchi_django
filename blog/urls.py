from django.urls import path
from . import views

urlpatterns = [
    path('royxatdan-otish/', views.royxatdan_otish, name='royxatdan_otish'),
    path('kirish/', views.kirish, name='kirish'),
    path('chiqish/', views.chiqish, name='chiqish'),

    # Put specific URL BEFORE <str:username>
    path('profil/tahrirlash/', views.profil_tahrirlash, name='profil_tahrirlash'),
    path('profil/<str:username>/', views.profil, name='profil'),

    path('', views.bosh_sahifa, name='bosh_sahifa'),
    path('biz-haqimizda/', views.biz_haqimizda, name='biz_haqimizda'),
    path('post/<int:post_id>/', views.post_batafsil, name='post_batafsil'),
    path('yangi/', views.post_yaratish, name='post_yaratish'),
    path('post/<int:post_id>/tahrirlash/', views.post_tahrirlash, name='post_tahrirlash'),
    path('post/<int:post_id>/ochirish/', views.post_ochirish, name='post_ochirish'),
    path('ommabop/', views.ommabop_postlar, name='ommabop'),
    path('aloqa/', views.aloqa, name='aloqa'),
]